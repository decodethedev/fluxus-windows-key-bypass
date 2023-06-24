module.exports = {
  apps: [
    {
      name: "discord-bot",
      script: "bot.py",
      interpreter: "python3",
      watch: true,
      autorestart: true,
      ignore_watch: ["bypass.html"], // Add any files you want PM2 to ignore watching
    },
  ],
};
