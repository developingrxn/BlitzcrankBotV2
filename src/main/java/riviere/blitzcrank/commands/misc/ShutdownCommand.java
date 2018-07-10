package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;
import riviere.blitzcrank.Blitzcrank;

import static java.lang.System.exit;

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
        blitzcrank.getShardManager().shutdown();
        exit(0);
    }
}
