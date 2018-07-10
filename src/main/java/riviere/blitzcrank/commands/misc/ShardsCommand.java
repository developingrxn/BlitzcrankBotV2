package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import riviere.blitzcrank.Blitzcrank;


public class ShardsCommand extends Command {
    private final Blitzcrank blitzcrank;

    public ShardsCommand(Blitzcrank blitzcrank) {
        this.name = "shards";
        this.ownerCommand = true;
        this.guildOnly = false;
        this.blitzcrank = blitzcrank;
    }

    @Override
    protected void execute(CommandEvent event) {
        if (event.getArgs().equals("restart")) restart();
        String message = "";
        for (int i = 0; i < blitzcrank.getShardManager().getShards().size(); i++) {
            message += "Shard " + i + ": " + blitzcrank.getShardManager().getShardById(i).getStatus() + " " + blitzcrank.getShardManager().getShardById(i).getPing() + "\n";
        }
        event.reply(message);
    }

    private void restart() {
        for (int i = 0; i < blitzcrank.getShardManager().getShards().size(); i++) {
            blitzcrank.getShardManager().restart(i);
        }
    }
}
