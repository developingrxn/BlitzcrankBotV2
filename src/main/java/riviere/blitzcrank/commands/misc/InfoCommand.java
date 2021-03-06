package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.JDAInfo;
import net.dv8tion.jda.core.Permission;

import com.sun.management.OperatingSystemMXBean;
import net.dv8tion.jda.core.entities.ChannelType;
import riviere.blitzcrank.Blitzcrank;

public class InfoCommand extends Command {
    private final OperatingSystemMXBean bean;
    private final Blitzcrank blitzcrank;

    public InfoCommand(Blitzcrank blitzcrank, OperatingSystemMXBean bean) {
        this.name = "info";
        this.help = "Gives basic information about the bot";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.aliases = new String[]{"about", "information"};
        this.bean = bean;
        this.blitzcrank = blitzcrank;
        this.guildOnly = false;
    }

    @Override
    protected void execute(CommandEvent event) {
        if (event.getSelfMember().hasPermission(event.getTextChannel(), Permission.MESSAGE_EMBED_LINKS) || event.isFromType(ChannelType.PRIVATE)) {
            long usedRAM = bean.getTotalPhysicalMemorySize() - bean.getFreePhysicalMemorySize();
            long usedRAMGB = usedRAM / 1000000000;
            JDA.ShardInfo si = event.getJDA().getShardInfo();
            EmbedBuilder builder = new EmbedBuilder();
            System.out.println(blitzcrank.getShardManager().getShardsRunning());
            builder.setColor(0x1AFFA7)
                    .setAuthor("Blitzcrank Bot - About:", null, event.getSelfUser().getAvatarUrl())
                    .setDescription("A simple bot in its third iteration for League of Legends summoner lookups")
                    .addField("Servers:", "" + blitzcrank.getShardManager().getGuilds().size(), true)
                    .addField("Shards:", "" + (si == null ? "1/1" : (si.getShardId()+1)+"/"+si.getShardTotal()), true)
                    .addField("RAM:", usedRAMGB + "/" + bean.getTotalPhysicalMemorySize() / 1000000000 + "GB", true)
                    .setFooter("Written by Frosty ☃#0141 | JDA " + JDAInfo.VERSION, null);

            event.reply(builder.build());

        } else event.reply("A simple bot in its third iteration for League of Legends summoner lookups. Written in Java using JDA by Frosty ☃#0141");
    }
}
