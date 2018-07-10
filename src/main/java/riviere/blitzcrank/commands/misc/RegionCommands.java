package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import riviere.blitzcrank.database.Database;

import java.sql.SQLException;


public class RegionCommands extends Command {
    private final Database db;

    public RegionCommands(Database db) {
        this.name = "region";
        this.help = "Commands for default region";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = true;
        this.db = db;
    }

    @Override
    public void execute(CommandEvent event) {
        String[] args = event.getArgs().split(" ");
        switch (args[0]) {
            case "view":
                view(event, event.getGuild().getId());
                break;
            case "set":
                set(event, event.getGuild().getId());
                break;
            case "update":
                update(event, event.getGuild().getId());
                break;
            case "list":
                list(event);
                break;
            default:
                event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setDescription("Available region commands are: `list, view, set, update`").build(), "```\nAvailable region commands are: list, view, set, update\n```");
                break;
        }
    }

    private void view(CommandEvent event, String guildID) {
        String region;
        try {
            region = db.findEntry(guildID);
        } catch (Exception e) {
            event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle("No region set!").build(), "```\nNo region set!\n```");
            return;
        }
        event.replyOrAlternate(new EmbedBuilder().setColor(0x1AFFA7).setTitle(region).build(), "```\n" + region +"\n```");
    }

    private void set(CommandEvent event, String guildID) {
        String[] validRegions = {"BR", "EUW", "EUNE", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"};
        String regionGiven = event.getArgs().split(" ")[1].toUpperCase();
        if (!(String.join(" ", validRegions).contains(regionGiven))) {
            event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle(String.format("%s is not a valid region!", regionGiven)).build(), "```\n" + regionGiven + " is not a valid region!\n```");
        } else {
            try {
                 String regionFound = db.findEntry(guildID);
                 event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle(regionFound + " is already the set region!").build(), "```\n" + regionFound + " is already the set region!\n```");
            } catch (SQLException e) {
                db.addEntry(guildID, event.getArgs().split(" ")[1].toUpperCase());
                event.replyOrAlternate(new EmbedBuilder().setColor(0x1AFFA7).setTitle("Done!").build(), "```\nDone!\n```");
            }
        }
    }

    private void update(CommandEvent event, String guildID) {
        String[] validRegions = {"BR", "EUW", "EUNE", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"};
        String regionGiven = event.getArgs().split(" ")[1].toUpperCase();
        if (!(String.join(" ", validRegions).contains(regionGiven))) {
            event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle(String.format("%s is not a valid region!", regionGiven)).build(), "```\n" + regionGiven + " is not a valid region!\n```");
        } else {
            try {
                db.findEntry(guildID);
                db.updateEntry(guildID, regionGiven);
                event.replyOrAlternate(new EmbedBuilder().setColor(0x1AFFA7).setTitle("Done!").build(), "```\nDone!\n```");
            } catch (SQLException e) {
                event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle("No region has been set yet!").build(), "```\nNo region has been set yet!\n```");
            }
        }
    }

    private void list(CommandEvent event) {
        event.replyOrAlternate(new EmbedBuilder().setColor(0x1AFFA7).setTitle("Valid Regions:").setDescription("BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR").build(), "```\nValid Regions:\nBR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR\n```");
    }
}
