package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.entities.ChannelType;

import java.time.Duration;
import java.time.LocalDateTime;

public class UptimeCommand extends Command {
    private final LocalDateTime start;

    public UptimeCommand(LocalDateTime start) {
        this.name = "uptime";
        this.help = "Gives the bot's uptime";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.start = start;
    }

    @Override
    protected void execute(CommandEvent event) {
        LocalDateTime end = LocalDateTime.now();
        Duration uptime = Duration.between(start, end);
        long seconds = uptime.getSeconds();

        String formatted = String.format(
                "%d day(s), %d:%02d:%02d",
                seconds / 86400,
                seconds / 3600,
                (seconds % 3600) / 60,
                seconds % 60
        );

        if (event.getSelfMember().hasPermission(Permission.MESSAGE_EMBED_LINKS) || event.isFromType(ChannelType.PRIVATE)) {
            EmbedBuilder builder = new EmbedBuilder();
            builder.setColor(0x1AFFA7)
                    .setTitle("Uptime:")
                    .setDescription(formatted);
            event.reply(builder.build());

        } else event.reply("Uptime: " + formatted);
    }
}
