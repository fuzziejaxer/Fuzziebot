require 'discordrb'

bot = Discordrb::Commands::CommandBot.new token: "", client_id: "", prefix: '+'

bot.command :ping do |msg|
    msg.respond "Pong!"
end


at_exit { bot.stop }
bot.run
