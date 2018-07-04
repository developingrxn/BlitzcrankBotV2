package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import net.dv8tion.jda.core.Permission;

import java.time.temporal.ChronoUnit;

public class PingCommand extends Command {

    public PingCommand() {
        this.name = "ping";
        this.help = "Tests the bot's latency";
        this.botPermissions = new Permission[]{Permission.MESSAGE_WRITE};
        this.guildOnly = false;
        this.aliases = new String[]{"pong", "pang", "peng"};
    }

    @Override
    protected void execute(CommandEvent event) {
        event.reply("Ponging ...", m -> {
            long ping = event.getMessage().getCreationTime().until(m.getCreationTime(), ChronoUnit.MILLIS);
            m.editMessage("Pong! " + ping  + "ms | Websocket: " + event.getJDA().getPing() + "ms").queue();
        });
    }
}

