package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import riviere.blitzcrank.Blitzcrank;

public class ShutdownCommand extends Command {
    private final Blitzcrank blitzcrank;

    public ShutdownCommand(Blitzcrank blitzcrank) {
        this.name = "shutdown";
        this.help = "Shuts down the bot";
        this.ownerCommand = true;
        this.blitzcrank = blitzcrank;
    }

    @Override
    protected void execute(CommandEvent event) {
        for (int i = 0; i < blitzcrank.getShardManager().getGuilds().size(); i++) {
            blitzcrank.getShardManager().shutdown(i);
        }
    }
}
