package riviere.blitzcrank;

class BlitzcrankShard {
    private long lastJDAEventTime;
    private final int shard;

    public BlitzcrankShard(int shardID) {
        this.lastJDAEventTime = System.currentTimeMillis();
        this.shard = shardID;
    }

    public long getLastJDAEventTime() {
        return lastJDAEventTime;
    }

    public void setLastJDAEventTime(long time) {
        this.lastJDAEventTime = time;
    }

    public int getShard() {
        return this.shard;
    }
}
