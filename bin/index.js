#!/usr/bin/env node

const { program } = require('commander');
const inquirer = require('inquirer').default || require('inquirer');
const chalk = require('chalk');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// Configuration - Replace this with your actual repo URL when publishing
const DEFAULT_REPO_URL = 'https://github.com/Hudda9000/skills.git';

async function run() {
  program
    .version('1.0.0')
    .description('Install opencode skills personally or to a repository');

  program
    .option('-r, --repo <url>', 'Source repository URL', DEFAULT_REPO_URL)
    .option('-p, --personal', 'Install to personal configuration (~/.config/opencode/skills)')
    .option('-l, --local', 'Install to local repository (.opencode/skills)')
    .option('-t, --target <target>', 'Harness target (agents, opencode, claude, codex)', 'opencode');

  program.parse(process.argv);
  const options = program.opts();

  let mode = options.personal ? 'personal' : (options.local ? 'local' : null);
  let selectedTarget = options.target || 'opencode';

  if (!mode) {
    const modeAnswers = await inquirer.prompt([
      {
        type: 'select',
        name: 'mode',
        message: 'Select installation mode:',
        choices: [
          { name: 'Personal (~/.config/...)', value: 'personal' },
          { name: 'Repository (./...)', value: 'local' }
        ]
      }
    ]);
    mode = modeAnswers.mode;
  }

  if (!options.target) {
    const targetAnswers = await inquirer.prompt([
      {
        type: 'select',
        name: 'target',
        message: 'Select harness target:',
        choices: [
          { name: '.agents', value: 'agents' },
          { name: 'OpenCode', value: 'opencode' },
          { name: 'Claude', value: 'claude' },
          { name: 'Codex', value: 'codex' }
        ]
      }
    ]);
    selectedTarget = targetAnswers.target;
  }

  const baseDir = mode === 'personal' ? path.join(os.homedir(), '.config') : process.cwd();
  const targetDir = path.join(baseDir, `.${selectedTarget}`, 'skills');

  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-install-'));

  try {
    console.log(chalk.blue(`Cloning skills from ${repoUrl}...`));
    execSync(`git clone --depth 1 ${repoUrl} ${path.join(tempDir, 'repo')}`, { stdio: 'inherit' });

    const skillsSrc = path.join(tempDir, 'repo', 'skills');
    if (!fs.existsSync(skillsSrc)) {
      console.error(chalk.red('Error: "skills/" directory not found in the repository.'));
      process.exit(1);
    }

    const availableSkills = fs.readdirSync(skillsSrc).filter(file => 
      fs.statSync(path.join(skillsSrc, file)).isDirectory()
    );

    if (availableSkills.length === 0) {
      console.log(chalk.yellow('No skills found in the repository.'));
      return;
    }

    const { selectedSkills } = await inquirer.prompt([
      {
        type: 'checkbox',
        name: 'selectedSkills',
        message: 'Select skills to install:',
        choices: availableSkills,
        pageSize: 15
      }
    ]);

    if (selectedSkills.length === 0) {
      console.log(chalk.yellow('No skills selected. Exiting.'));
      return;
    }

    console.log(chalk.blue(`\nTarget directory: ${targetDir}`));
    fs.mkdirSync(targetDir, { recursive: true });

    for (const skill of selectedSkills) {
      console.log(chalk.green(`Installing skill: ${skill}...`));
      const dest = path.join(targetDir, skill);
      
      // Remove existing to ensure clean install
      if (fs.existsSync(dest)) {
        fs.rmSync(dest, { recursive: true, force: true });
      }
      
      fs.cpSync(path.join(skillsSrc, skill), dest, { recursive: true });
    }

    console.log(chalk.bold.green('\nInstallation complete! 🎉'));
  } catch (error) {
    console.error(chalk.red(`\nAn error occurred during installation:`), error.message);
    try {
      execSync('rm -rf ' + tempDir);
    } catch (e) {}
    process.exit(1);
  } finally {
    // Cleanup is handled by the trap in shell, but here we do it explicitly if not using tempDir as a single object
    // However, since we used fs.mkdtempSync, we should clean up.
    try {
      fs.rmSync(tempDir, { recursive: true, force: true });
    } catch (e) {}
  }
}

run();
