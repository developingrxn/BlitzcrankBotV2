package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.entities.ChannelType;

public class InviteCommand extends Command {

    public InviteCommand() {
        this.name = "invite";
        this.help = "Gives the bot's invite link";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = false;
    }

    @Override
    protected void execute(CommandEvent event) {
        String inviteURL = "https://discordapp.com/oauth2/authorize?client_id=282765243862614016&scope=bot&permissions=19456";

        if (event.getSelfMember().hasPermission(Permission.MESSAGE_EMBED_LINKS) || event.isFromType(ChannelType.PRIVATE)) {
            EmbedBuilder builder = new EmbedBuilder();
            builder.setColor(0x1AFFA7)
                    .setDescription("[Click here to invite me to your server!](" + inviteURL + ")");
            event.reply(builder.build());

        } else event.reply("Click here to invite me to your server: " + inviteURL);

    }
}
