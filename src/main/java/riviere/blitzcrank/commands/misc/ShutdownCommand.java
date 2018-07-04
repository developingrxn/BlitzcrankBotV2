package riviere.blitzcrank.commands.misc;

import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandEvent;

public class ShutdownCommand extends Command {
    public ShutdownCommand() {
        this.name = "shutdown";
        this.help = "Shuts down the bot";
        this.ownerCommand = true;
    }

    @Override
    protected void execute(CommandEvent event) { event.getJDA().shutdown(); }
}
