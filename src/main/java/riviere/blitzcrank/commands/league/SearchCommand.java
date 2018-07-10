package riviere.blitzcrank.commands.league;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import com.merakianalytics.orianna.Orianna;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.BadRequestException;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.ForbiddenException;
import com.merakianalytics.orianna.datapipeline.riotapi.exceptions.NotFoundException;
import com.merakianalytics.orianna.types.common.Region;
import com.merakianalytics.orianna.types.common.Season;
import com.merakianalytics.orianna.types.core.league.LeaguePosition;
import com.merakianalytics.orianna.types.core.league.LeaguePositions;
import com.merakianalytics.orianna.types.core.summoner.Summoner;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.entities.Message;

public class SearchCommand extends Command {
    private final ArgumentParser ap;

    public SearchCommand(ArgumentParser ap) {
        this.name = "search";
        this.help = "Gets ranked stats for a summoner";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = true;
        this.aliases = new String[]{"lookup", "find", "stats"};
        this.arguments = "[user] [region]";
        this.ap = ap;
    }

    @Override
    protected void execute(CommandEvent event) {
        event.async(() -> {
            boolean hasPerms =event.getSelfMember().hasPermission(Permission.MESSAGE_EMBED_LINKS);
            Message msg;
            if (hasPerms) {
                msg = event.getChannel().sendMessage(new EmbedBuilder().setTitle("Rocket grabbing your data...", null).setColor(0xFCC932).build()).complete();
            } else {
                msg = event.getChannel().sendMessage("```\nRocket grabbing your data...\n```").complete();
            }
            String[] args = ap.parseArgs(event.getArgs(), event.getGuild().getId(), false);
            if (args.length == 0) return;
            if (args[2] == null) {
                msg.editMessage("No region specified, and no default region set!").queue();
                return;
            }

            try {
                Summoner summoner = Orianna.summonerNamed(args[0]).withRegion(Region.valueOf(args[2])).get();

                // 0 - Name of queue
                // 1 - Tier and Division
                // 2 - Current LP
                // 3 - Number of wins
                // 4 - Number of losses
                // 5 - in promos or not
                // 6 - promos progress
                String[] solo = new String[7];
                String[] flex = new String[7];
                String[] threes = new String[7];
                solo[0] = "Ranked Solo:";
                flex[0] = "Ranked Flex:";
                threes[0] = "Ranked 3s:";

                final LeaguePositions positions = summoner.getLeaguePositions();
                for (final LeaguePosition position : positions) {
                    String name = position.getQueue().name();
                    switch (name) {
                        case "RANKED_SOLO_5x5":
                            solo[1] = ToTitleCase.toTitleCase(position.getTier().toString()) + " " + position.getDivision();
                            solo[2] = "" + position.getLeaguePoints();
                            solo[3] = "" + position.getWins();
                            solo[4] = "" + position.getLosses();
                            solo[5] = position.getPromos() == null ? null : "yes";
                            if (solo[5] != null) {
                                solo[6] = position.getPromos().getProgess().replace("N", "- ").replace("W", "✔ ").replace("L", "X ");
                            }
                            break;
                        case "RANKED_FLEX_5x5":
                            flex[1] = ToTitleCase.toTitleCase(position.getTier().toString()) + " " + position.getDivision();
                            flex[2] = "" + position.getLeaguePoints();
                            flex[3] = "" + position.getWins();
                            flex[4] = "" + position.getLosses();
                            flex[5] = position.getPromos() == null ? null : "yes";
                            if (flex[5] != null) {
                                flex[6] = position.getPromos().getProgess().replace("N", "- ").replace("W", "✔ ").replace("L", "X ");
                            }
                            break;
                        case "RANKED_FLEX_TT":
                            threes[1] = ToTitleCase.toTitleCase(position.getTier().toString()) + " " + position.getDivision();
                            threes[2] = "" + position.getLeaguePoints();
                            threes[3] = "" + position.getWins();
                            threes[4] = "" + position.getLosses();
                            threes[5] = position.getPromos() == null ? null : "yes";
                            if (threes[5] != null) {
                                threes[6] = position.getPromos().getProgess().replace("N", "- ").replace("W", "✔ ").replace("L", "X ");
                            }
                            break;
                    }
                }


                String[][] queues = new String[3][7];
                queues[0] = solo;
                queues[1] = flex;
                queues[2] = threes;

                if (hasPerms) {
                    EmbedBuilder builder = new EmbedBuilder();

                    for (String[] queue : queues) {
                        if (queue[1] == null) continue;
                        float winrate = Float.parseFloat(queue[3]) / (Float.parseFloat(queue[3]) + Float.parseFloat(queue[4])) * 100;
                        builder.addField(queue[0], String.format("%s - %sLP", queue[1], queue[2]), true);
                        builder.addField("W/L", String.format("%sW - %sL (%.0f%%)", queue[3], queue[4], winrate), true);
                        if (queue[5] != null) {
                            builder.addField("Promos Progress:", queue[6], true);
                            builder.addBlankField(true);
                        }
                    }

                    builder.setColor(0x1AFFA7)
                            .setAuthor(String.format("Summoner Lookup - %s (%s)", args[0], args[2]))
                            .setDescription(String.format("Level %d", summoner.getLevel()))
                            .setTitle(String.format("Season 7 %s", summoner.getHighestTier(Season.SEASON_8) == null ? "Unranked" : ToTitleCase.toTitleCase(summoner.getHighestTier(Season.SEASON_8).toString())))
                            .setThumbnail(summoner.getProfileIcon() == null ? "http://ddragon.leagueoflegends.com/cdn/8.13.1/img/profileicon/0.png" : summoner.getProfileIcon().getImage().getURL());
                    msg.editMessage(builder.build()).queue();

                } else {
                    String message = "```\n";
                    message += String.format("Summoner Lookup - %s (%s)\n", args[0], args[2]);
                    message += String.format("Level:%19d\n", summoner.getLevel());
                    message += String.format("Season 7:%16s\n", ToTitleCase.toTitleCase(summoner.getHighestTier(Season.SEASON_8).toString()));
                    message += String.format("Ranked Solo:%13s\n", solo[1]);
                    message += String.format("Ranked Flex:%13s\n", flex[1]);
                    message += String.format("Ranked 3s:%15s\n", threes[1]);
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
