package riviere.blitzcrank.database;

import riviere.blitzcrank.commands.league.ToTitleCase;

import java.sql.*;

public class Database {


    private Connection connect() {
        Connection conn;
        try {
            String url = "jdbc:sqlite:/home/alex_palmer/guilds.db";
            conn = DriverManager.getConnection(url);
            return conn;
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public void addGuild(String guildID) {
        try {
            Connection conn = this.connect();
            Statement stmt = conn.createStatement();
            stmt.execute(String.format("CREATE TABLE %s(sum_name TEXT, region TEXT)", "_" + guildID));
            stmt.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void addUser(String guildID, String summoner, String region) {
        try {
            Connection conn = this.connect();
            PreparedStatement stmt = conn.prepareStatement(String.format("INSERT INTO %s(sum_name, region) VALUES(?,?)", "_" + guildID));
            stmt.setString(1, ToTitleCase.toTitleCase(summoner));
            stmt.setString(2, region);
            stmt.executeUpdate();
            stmt.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void addEntry(String guildID, String region) {
        try {
            Connection conn = this.connect();
            PreparedStatement stmt = conn.prepareStatement("INSERT INTO guilds(guild_id, region) VALUES(?,?)");
            stmt.setString(1, guildID);
            stmt.setString(2, region);
            stmt.executeUpdate();
            stmt.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void updateEntry(String guildID, String region) {
        try {
            Connection conn = this.connect();
            PreparedStatement stmt = conn.prepareStatement("UPDATE guilds SET region = ? WHERE guild_id = ?");
            stmt.setString(1, region);
            stmt.setString(2, guildID);
            stmt.executeUpdate();
            stmt.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public String findEntry(String guildID) throws SQLException {
        try {
            Connection conn = this.connect();
            PreparedStatement stmt = conn.prepareStatement("SELECT region FROM guilds WHERE guild_id = ?");
            stmt.setString(1, guildID);
            ResultSet rs = stmt.executeQuery();
            String region = rs.getString(1);
            rs.close();
            stmt.close();
            conn.close();
            return region;
        } catch (SQLException e) {
            throw e;
        }
    }
}
