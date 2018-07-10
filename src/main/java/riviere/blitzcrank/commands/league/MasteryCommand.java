package riviere.blitzcrank.commands.league;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import com.merakianalytics.orianna.Orianna;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.BadRequestException;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.ForbiddenException;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.NotFoundException;
import com.merakianalytics.orianna.types.common.Region;
import com.merakianalytics.orianna.types.core.championmastery.ChampionMastery;
import com.merakianalytics.orianna.types.core.staticdata.Champion;
import com.merakianalytics.orianna.types.core.summoner.Summoner;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.entities.Message;
import org.joda.time.DateTime;

public class MasteryCommand extends Command {
    private final ArgumentParser ap;

    public MasteryCommand(ArgumentParser ap) {
        this.name = "mastery";
        this.help = "Gets champion mastery for a summoner";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = true;
        this.aliases = new String[]{"champion", "champ"};
        this.ap = ap;
    }

    @Override
    protected void execute(CommandEvent event) {
        event.async(() -> {
            boolean hasPerms = event.getSelfMember().hasPermission(Permission.MESSAGE_EMBED_LINKS);
            Message msg;
            if (hasPerms) {
                msg = event.getChannel().sendMessage(new EmbedBuilder().setTitle("Rocket grabbing your data...", null).setColor(0xFCC932).build()).complete();
            } else {
                msg = event.getChannel().sendMessage("```\nRocket grabbing your data...\n```").complete();
            }

            String[] args = ap.parseArgs(event.getArgs(), event.getGuild().getId(), true);
            if (args.length < 2) return;
            if (args[2] == null) {
                msg.editMessage("No region specified, and no default region set!").queue();
                return;
            }
            try {
                Summoner summoner = Orianna.summonerNamed(args[0]).withRegion(Region.valueOf(args[2])).get();
                Champion champion = Orianna.championNamed(args[1]).withRegion(Region.valueOf(args[2])).get();
                try {
                    champion.load();
                } catch (NullPointerException e) {
                    if (hasPerms) msg.editMessage(new EmbedBuilder().setColor(0xCA0147).setTitle("404: Not Found!").setDescription("Invalid champion!").build()).queue();
                    else msg.editMessage("```\nInvalid champion!\n```").queue();
                    return;
                }

                ChampionMastery mastery = summoner.getChampionMastery(champion);
                int masteryLevel = mastery.getLevel();
                int masteryPoints = mastery.getPoints();
                DateTime timeLastPlayed = mastery.getLastPlayed();
                if (hasPerms) {
                    EmbedBuilder builder = new EmbedBuilder();
                    builder.setAuthor(String.format("%s Mastery - %s (%s)", champion.getName(), summoner.getName(), summoner.getRegion()), null, champion.getImage().getURL())
                            .setColor(0x1AFFA7)
                            .addField("Champion Level:", "" + masteryLevel, true)
                            .addField("Mastery Points", "" + masteryPoints, true)
                            .addField("Last Played:", timeLastPlayed.toString("yyyy-MM-dd"), true);
                    msg.editMessage(builder.build()).queue();
                } else {
                    String message = "```\n";
                    message += String.format("%s Mastery - %s (%s):\n", champion.getName(), summoner.getName(), summoner.getRegion());
                    message += String.format("Champion Level:%10s\n", masteryLevel);
                    message += String.format("Mastery Points:%10s\n", masteryPoints);
                    message += String.format("Last Played:%13s\n",  timeLastPlayed.toString("yyyy-MM-dd"));
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
        });
    }
}
