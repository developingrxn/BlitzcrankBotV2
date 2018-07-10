package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.Permission;
import riviere.blitzcrank.Blitzcrank;


import java.time.temporal.ChronoUnit;

public class PingCommand extends Command {
    private final Blitzcrank blitzcrank;

    public PingCommand(Blitzcrank blitzcrank) {
        this.name = "ping";
        this.help = "Tests the bot's latency";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = false;
        this.aliases = new String[]{"pong", "pang", "peng"};
        this.blitzcrank = blitzcrank;
    }

    @Override
    protected void execute(CommandEvent event) {
        event.reply("Ponging ...", m -> {
            long ping = event.getMessage().getCreationTime().until(m.getCreationTime(), ChronoUnit.MILLIS);
            m.editMessage("Pong! This shard: " + ping  + "ms | All shards: " + Math.round(blitzcrank.getShardManager().getAveragePing()) + "ms | Websocket: " + event.getJDA().getPing() + "ms").queue();

        });
    }
}

