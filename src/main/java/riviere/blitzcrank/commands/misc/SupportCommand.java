package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.entities.ChannelType;

public class SupportCommand extends Command {

    public SupportCommand() {
        this.name = "support";
        this.help = "Gives a link to the bot's support server";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = false;
    }

    @Override
    protected void execute(CommandEvent event) {
        String supportURL = "https://discord.gg/UP4TwFX";

        if (event.getSelfMember().hasPermission(Permission.MESSAGE_EMBED_LINKS) || event.isFromType(ChannelType.PRIVATE)) {
            EmbedBuilder builder = new EmbedBuilder();
            builder.setColor(0x1AFFA7)
                    .setDescription("[Click here to join my support server!](" + supportURL + ")");
            event.reply(builder.build());
        } else {
            event.reply("Click here to join my support server: " + supportURL);
        }
    }
}
