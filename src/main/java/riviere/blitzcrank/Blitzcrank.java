package riviere.blitzcrank;

import com.jagrosh.jdautilities.command.CommandClientBuilder;
import com.merakianalytics.orianna.Orianna;
import com.merakianalytics.orianna.types.common.Region;
import com.sun.management.OperatingSystemMXBean;
import net.dv8tion.jda.bot.sharding.DefaultShardManagerBuilder;
import net.dv8tion.jda.bot.sharding.ShardManager;
import net.dv8tion.jda.core.OnlineStatus;
import net.dv8tion.jda.core.entities.Game;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import riviere.blitzcrank.commands.league.ArgumentParser;
import riviere.blitzcrank.commands.league.CurrentGameCommand;
import riviere.blitzcrank.commands.league.MasteryCommand;
import riviere.blitzcrank.commands.league.SearchCommand;
import riviere.blitzcrank.commands.misc.*;
import riviere.blitzcrank.database.Database;

import javax.security.auth.login.LoginException;
import java.io.File;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.stream.Collectors;

public class Blitzcrank {
    private ShardManager shards = null;
    private final static Logger LOG = LoggerFactory.getLogger(Blitzcrank.class);

    private Blitzcrank() throws IOException, LoginException {
        // should have five lines
        // 0 - bot token
        // 1 - riot api key
        // 2 - db api key
        // 3 - dbl api key
        // 4 - bot owner
        List<String> tokens;
        try {
             tokens = Files.readAllLines(Paths.get("config.txt"));
        } catch (NoSuchFileException e) {
            System.out.println("Required config file missing, aborting");
            return;
        }

        String botToken = tokens.get(0);
        String riotAPIKey = tokens.get(1);
        String dbAPIKey = tokens.get(2);
        String dblAPIKey = tokens.get(3);
        String ownerId = tokens.get(4);

        LocalDateTime start = LocalDateTime.now();
        OperatingSystemMXBean bean = (com.sun.management.OperatingSystemMXBean) ManagementFactory.getOperatingSystemMXBean();
        Orianna.loadConfiguration(new File("orianna-config.json"));
        Orianna.setRiotAPIKey(riotAPIKey);
        String game = "b!help | Fleshling Compatibility Service";
        Database db = new Database();
        ArgumentParser ap = new ArgumentParser(db);

        CommandClientBuilder client = new CommandClientBuilder()
                .setOwnerId(ownerId)
                .setPrefix("b!")
                .setAlternativePrefix("@mention")
                .useHelpBuilder(false)
                .setDiscordBotsKey(dbAPIKey)
                .setDiscordBotListKey(dblAPIKey)
                .setGame(Game.playing(game));

        client.addCommands(
                // league commands
                new SearchCommand(ap),
                new MasteryCommand(ap),
                new CurrentGameCommand(ap),

                //misc commands
                new PingCommand(),
                new InviteCommand(),
                new SupportCommand(),
                new HelpCommand(),
                new UptimeCommand(start),
                new ShutdownCommand(this),
                new InfoCommand(this, bean),
                new RegionCommands(db),
                new ShardsCommand(this)
        );

        Orianna.setRiotAPIKey(riotAPIKey);
        Orianna.setDefaultRegion(Region.NORTH_AMERICA);

        shards = new DefaultShardManagerBuilder()
                .setToken(botToken)
                .setStatus(OnlineStatus.DO_NOT_DISTURB)
                .setGame(Game.playing("loading..."))
                .build();

        List<BlitzcrankShard> blitzcrankShards = new ArrayList<>();
        for (int i = 0; i < shards.getShardsTotal(); i++) {
            BlitzcrankShard shard = new BlitzcrankShard(i);
            shards.getShardById(i).setEventManager(new ShardEventManager(shard));
            System.out.println(i);
            shards.addEventListener(new Listener(this), client.build());
            blitzcrankShards.add(shard);
            try {
                Thread.sleep(5000L);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

       new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(600000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                LOG.info("Checking for zombie shards...");
                final List<BlitzcrankShard> deadShards = blitzcrankShards.stream()
                        .filter(e -> System.currentTimeMillis() - e.getLastJDAEventTime() > 300000).collect(Collectors.toList());
                if (!deadShards.isEmpty()) {
                    LOG.info("Resurrecting zombie shards: " + Arrays.toString(deadShards.stream()
                            .map(e -> "#" + e.getShard() + ": " + e.getLastJDAEventTime()).toArray()));
                    final Collection<Integer> shardsToRebuild = new CopyOnWriteArrayList<>();
                    deadShards.forEach(shard -> {
                        shardsToRebuild.add(shard.getShard());
                        shards.shutdown(shard.getShard());
                    });
                    shardsToRebuild.forEach(shard -> {
                        blitzcrankShards.removeIf(e -> e.getShard() == shard);
                        final BlitzcrankShard newShard = new BlitzcrankShard(shard);
                        blitzcrankShards.add(newShard);
                        LOG.info("Resurrected shard " + shard);
                        shards.start(shard);
                        try {
                            Thread.sleep(5000L);
                        } catch(final InterruptedException e) {
                            e.printStackTrace();
                        }
                    });
                    blitzcrankShards.sort(Comparator.comparingInt(BlitzcrankShard::getShard));
                } else {
                    LOG.info("No zombie shards found!");
                }
            }
        }).start();
    }

    public ShardManager getShardManager() {
        return shards;
    }

    public static void main(String[] args) {
        try {
            new Blitzcrank();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }



}
