package riviere.blitzcrank;

import net.dv8tion.jda.core.events.Event;
import net.dv8tion.jda.core.events.StatusChangeEvent;
import net.dv8tion.jda.core.hooks.InterfacedEventManager;

class ShardEventManager extends InterfacedEventManager {
    private final BlitzcrankShard blitzcrankShard;

    public ShardEventManager(final BlitzcrankShard blitzcrankShard) {
        this.blitzcrankShard = blitzcrankShard;
    }

    @Override
    public void handle(final Event event) {
        super.handle(event);
        blitzcrankShard.setLastJDAEventTime(System.currentTimeMillis());
    }
}
