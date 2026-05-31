// PM2 config for Investment Research Engine
// Usage: pm2 start deploy/ecosystem.config.js
module.exports = {
  apps: [{
    name: 'investment-engine',
    script: 'server.py',
    interpreter: 'python3',
    cwd: '/opt/investment-engine',
    args: '',
    env: {
      PORT: 9001,
    },
    // Use uvicorn instead of direct python
    script: './start.sh',
    interpreter: 'bash',
    kill_timeout: 30000,
    max_restarts: 5,
    restart_delay: 3000,
  }]
};
