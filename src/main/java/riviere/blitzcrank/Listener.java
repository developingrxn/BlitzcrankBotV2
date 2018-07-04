package riviere.blitzcrank;


import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.JDA.ShardInfo;
import net.dv8tion.jda.core.entities.Guild;
import net.dv8tion.jda.core.entities.TextChannel;
import net.dv8tion.jda.core.events.Event;
import net.dv8tion.jda.core.events.ReadyEvent;
import net.dv8tion.jda.core.events.guild.GuildJoinEvent;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import net.dv8tion.jda.core.hooks.EventListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;




@SuppressWarnings("ConstantConditions")
class Listener implements EventListener {

    private final static Logger LOG = LoggerFactory.getLogger(Listener.class);

    @SuppressWarnings("ConstantConditions")
    @Override
    public void onEvent(Event event) {
        if (event instanceof ReadyEvent) {
            ShardInfo si = event.getJDA().getShardInfo();
            String shardInfo = si==null ? "1/1" : (si.getShardId()+1)+"/"+si.getShardTotal();
            LOG.info("Shard " + shardInfo + " is ready");

        } else if (event instanceof GuildJoinEvent) {
            Guild guild = ((GuildJoinEvent) event).getGuild();
            int botCount = (int) guild.getMembers().stream().filter((member -> member.getUser().isBot())).count();
            if (guild.getMembers().size() - botCount < 5 || (botCount > 20) && ((double) botCount / guild.getMembers().size() > 0.65)) {
                guild.getDefaultChannel().sendMessage("In order to reduce my load, I leave servers that waste my resources, sorry :(").queue();
                guild.leave().queue();

                EmbedBuilder builder = new EmbedBuilder();
                builder.setColor(0x1AFFA7)
                        .setTitle("Left Server")
                        .addField("Server:", guild.getName(), true)
                        .addBlankField(true)
                        .addField("Users:", "" + guild.getMembers().size(), true)
                        .addField("Bots", "" + botCount, true);
                TextChannel log = event.getJDA().getTextChannelById("295831639219634177");
                log.sendMessage(builder.build()).queue();
            } else {
                //noinspection ConstantConditions
                guild.getDefaultChannel().sendMessage("Beep, boop! To set up a default LoL region for my lookup commands, please use the `b!region set` command! (Example, `b!region set OCE`)").queue();

                EmbedBuilder builder = new EmbedBuilder();
                builder.setColor(0x1AFFA7)
                        .setTitle("Joined Server")
                        .addField("Server:", guild.getName(), true)
                        .addBlankField(true)
                        .addField("Users:", "" + guild.getMembers().size(), true)
                        .addField("Total:", "" + event.getJDA().getGuilds().size(), true);
                TextChannel log = event.getJDA().getTextChannelById("295831639219634177");
                log.sendMessage(builder.build()).queue();
            }

        } else if (event instanceof MessageReceivedEvent) {
            if (((MessageReceivedEvent) event).getMessage().getContentRaw().startsWith("b!")) {
                LOG.info(((MessageReceivedEvent) event).getAuthor().getName() + " (in " + ((MessageReceivedEvent) event).getGuild().getName() + ": " + ((MessageReceivedEvent) event).getChannel().getName() + "): " + ((MessageReceivedEvent) event).getMessage().getContentDisplay());
            }
        }
    }
}
