require('dotenv').config();
const Telegraf = require('telegraf')
const Extra = require('telegraf/extra')
const session = require('telegraf/session')
const express = require('express')
const bodyParser = require('body-parser');
const { reply, fork } = Telegraf

const bot = new Telegraf(process.env.BOT_TOKEN)
const app = express()

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

bot.use(session())

bot.telegram.setWebhook('https://luftaquila.io/api/telepath/report')
app.use(bot.webhookCallback('/report'))

bot.start(function(ctx) {
  ctx.reply('Your chat ID:');
  ctx.reply(ctx.chat.id);
});
bot.on('text', function(ctx) {
  ctx.reply('Your chat ID:');
  ctx.reply(ctx.chat.id);
});

// Launch bot
bot.launch()
app.listen(3161);

app.post('//report', function(req, res) {
  bot.telegram.sendMessage(req.body.destination, '<b>' + req.body.date + '</b>', {parse_mode: 'HTML'});
  setTimeout(function() {
    for(let item of JSON.parse(unescape(req.body.contents.replace(/\/\//, '%').replace(/\'/g, '"')))) {
      let payload = '<b><i>' + item.title + '</i></b>\n' + item.detail.replace(/<br \/>/g, '');
      bot.telegram.sendMessage(req.body.destination, payload, {parse_mode: 'HTML'});
    }
  }, 500);
  res.status(200).send();
});
