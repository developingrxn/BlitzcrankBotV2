package riviere.blitzcrank.commands.league;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import com.merakianalytics.orianna.Orianna;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.BadRequestException;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.ForbiddenException;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.NotFoundException;
import com.merakianalytics.orianna.types.common.Queue;
import com.merakianalytics.orianna.types.common.Region;
import com.merakianalytics.orianna.types.common.Season;
import com.merakianalytics.orianna.types.core.spectator.CurrentMatch;
import com.merakianalytics.orianna.types.core.spectator.CurrentMatchTeam;
import com.merakianalytics.orianna.types.core.spectator.Player;
import com.merakianalytics.orianna.types.core.summoner.Summoner;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.entities.Message;
import org.joda.time.Duration;

public class CurrentGameCommand extends Command {
    private ArgumentParser ap;

    public CurrentGameCommand(ArgumentParser ap) {
        this.name = "game";
        this.help = "Gets a summoner's current game";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = false;
        this.aliases = new String[]{"playing", "match"};
        this.ap = ap;
    }

    @Override
    protected void execute(CommandEvent event) {
        boolean hasPerms = event.getSelfMember().hasPermission(Permission.MESSAGE_EMBED_LINKS);
        Message msg = null;
        if (hasPerms) {
            msg = event.getChannel().sendMessage(new EmbedBuilder().setTitle("Rocket grabbing your data (this one takes a while)...", null).setColor(0xFCC932).build()).complete();
        } else {
            msg = event.getChannel().sendMessage("```\nRocket grabbing your data...\n```").complete();
        }
        event.getChannel().sendTyping().queue();
        String[] args = ap.parseArgs(event.getArgs(), event.getGuild().getId(), false);
        if (args.length == 0) return;
        if (args[2] == null) {
            msg.editMessage("No region specified, and no default region set!").queue();
            return;
        }
        try {
            Summoner summoner = Orianna.summonerNamed(args[0]).withRegion(Region.valueOf(args[2])).get();
            CurrentMatch currentGame = summoner.getCurrentMatch();
            try {
                currentGame.load();
            } catch (NotFoundException e) {
                if (hasPerms) msg.editMessage(new EmbedBuilder().setColor(0xCA0147).setTitle("Error!").setDescription(String.format("%s is not in an active game!", summoner.getName())).build()).queue();
                else msg.editMessage("```\nSummoner not in game!\n```").queue();
                return;
            }

            Queue queue = currentGame.getQueue();
            Duration duration = currentGame.getDuration();
            CurrentMatchTeam blueTeam = currentGame.getBlueTeam();
            CurrentMatchTeam redTeam = currentGame.getRedTeam();
            long seconds = duration.getMillis();
            String formatted = String.format(
                    "%02d:%02d",
                    (seconds % 3600) / 60,
                    seconds % 60
            );

            if (hasPerms) {
                EmbedBuilder builder = new EmbedBuilder();
                String blueField = "";
                String redField = "";
                for (Player player : blueTeam.getParticipants()) {
                    blueField += String.format("(%s) **%s**\n%s\n\n", player.getSummoner().getHighestTier(Season.SEASON_8) == null ? "Unranked" : ToTitleCase.toTitleCase(summoner.getHighestTier(Season.SEASON_8).toString()), player.getSummoner().getName(), player.getChampion().getName());
                }
                for (Player player : redTeam.getParticipants()) {
                    redField += String.format("(%s) **%s**\n%s\n\n", player.getSummoner().getHighestTier(Season.SEASON_8) == null ? "Unranked" : ToTitleCase.toTitleCase(summoner.getHighestTier(Season.SEASON_8).toString()), player.getSummoner().getName(), player.getChampion().getName());
                }
                builder.addField("Blue Team", blueField, true)
                        .addField("Red Team", redField, true);

                builder.setColor(0x1AFFA7)
                        .setAuthor(String.format("%s's Current %s Match (%s) - Duration: %s", summoner.getName(), queue.name(), summoner.getRegion(), formatted));
                msg.editMessage(builder.build()).queue();
            } else {
                String message = "```\n";
                String field = "";
                for (int i = 0; i < blueTeam.getParticipants().size(); i++) {
                    Player blue = blueTeam.getParticipants().get(i);
                    Player red = redTeam.getParticipants().get(i);
                    field += String.format("%1$-20s %2$20s\n%3$-20s%4$20s\n\n", blue.getSummoner().getName(), red.getSummoner().getName(), blue.getChampion().getName(), red.getChampion().getName());
                }
                message += field;
                message += "```";
                msg.editMessage(message).queue();
            }

        } catch (NotFoundException e) {
            if (msg != null) event.getChannel().deleteMessageById(msg.getId()).complete();
            event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle("404: Not Found!").setDescription("Could not find summoner :(").build(), "404: Not Found!");
        } catch (ForbiddenException e) {
            if (msg != null) event.getChannel().deleteMessageById(msg.getId()).complete();
            event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle("403: Forbidden!").setDescription("Either an illegal character was entered, or my API key has expired.").build(), "403: Forbidden!");
        } catch (BadRequestException e) {
            if (msg != null) event.getChannel().deleteMessageById(msg.getId()).complete();
            event.replyOrAlternate(new EmbedBuilder().setColor(0xCA0147).setTitle("400: Bad Request!").setDescription("Malformed request").build(), "400: Bad Request!");
        }


    }
}
