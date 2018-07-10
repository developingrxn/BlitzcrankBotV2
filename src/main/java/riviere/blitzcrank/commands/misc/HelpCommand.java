package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.entities.ChannelType;

public class HelpCommand extends Command {

    public HelpCommand() {
        this.name = "help";
        this.help = "Gives information on the bot's commands";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = false;
        this.arguments = "[more]";
    }

    @Override
    protected void execute(CommandEvent event) {
        String helpURL = "https://apal0934.github.io/BlitzcrankBotV2/";
        if (event.getSelfMember().hasPermission(event.getTextChannel(), Permission.MESSAGE_EMBED_LINKS) || event.isFromType(ChannelType.PRIVATE)) {
                if (event.getArgs().isEmpty()) {
                EmbedBuilder builder = new EmbedBuilder();
                builder.setColor(0x1AFFA7)
                        .setDescription("[Click here to view a full list of commands!](" + helpURL + ")")
                        .setAuthor("Blitzcrank Bot - Commands:", null, event.getSelfUser().getAvatarUrl())
                        .addField("b!search 'User'", "Show a user's ranked statistics", true)
                        .addField("Example:", "b!search Riviere", true)
                        .addField("b!mastery 'User' 'Champ'", "Shows a user's champ mastery", true)
                        .addField("Example:", "b!mastery Riviere Sivir", true)
                        .addField("b!game 'User'", "Look up a user's current match", true)
                        .addField("Example:", "b!game Riviere", true)
                        .addField("b!region view", "Show the default region", false)
                        .addField("b!region set 'region'", "Set the server's default region", true)
                        .addField("Example:", "b!region set OCE", true)
                        .addField("b!region list", "Show a list of all valid regions", false)
                        .addField("Other commands:", "Other commands can be listed with b!help more", true);
                event.reply(builder.build());
            } else if (event.getArgs().equals("more")){
                EmbedBuilder builder = new EmbedBuilder();
                builder.setColor(0x1AFFA7)
                        .setAuthor("Blitzcrank Bot - Commands:", null, event.getSelfUser().getAvatarUrl())
                        .addField("b!invite", "Invite Blitzcrank to your server!", false)
                        .addField("b!support", "Ask for help in the support server!", false)
                        .addField("b!ping", "Tests response time", false)
                        .addField("b!uptime", "Returns time since last reboot", false)
                        .addField("b!info", "Returns basic info about Blitzcrank", false);
                event.reply(builder.build());
            }
        } else {
            event.reply("View a full list of commands here: " + helpURL);
        }
    }
}
