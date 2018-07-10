package riviere.blitzcrank.commands.league;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import riviere.blitzcrank.database.Database;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@SuppressWarnings("ALL")
public class ArgumentParser {
    private final static String[] VALID_REGIONS = {"BR", "EUW", "EUNE", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"};
    private final Database db;

    public ArgumentParser(Database db) {
        this.db = db;
    }

    @SuppressWarnings("unused")
    enum Region {
        BR("BRAZIL"), EUW("EUROPE_WEST"), EUNE("EUROPE_NORTH_EAST"), JP("JP"), KR("KOREA"), LAN("LATIN_AMERICA_NORTH"),
        LAS("LATIN_AMERICA_SOUTH"), NA("NORTH_AMERICA"), OCE("OCEANIA"), RU("RUSSIA"), TR("TURKEY");

        private final String region;

        String getRegion() {
            return this.region;
        }

        Region(String region) {
            this.region = region;
        }
    }

    private final static Logger LOG = LoggerFactory.getLogger(ArgumentParser.class);

    public String[] parseArgs(String args, String guildID, boolean mastery) {
        List<String> tokens = new ArrayList<>(Arrays.asList(args.split(" ")));
        int size = tokens.size();
        String[] parsedArgs = {null, null, null};

        for (String validRegion : VALID_REGIONS) {
            if (validRegion.equals(tokens.get(size - 1).toUpperCase())) {
                Region region = Region.valueOf(validRegion);
                parsedArgs[2] = region.getRegion();
                break;
            }
        }
        if (mastery) {
            try {
                List<String> spaces = Files.readAllLines(Paths.get("spaces.txt"));
                for (String champs : spaces) {
                   if (parsedArgs[2] == null) {
                       if (champs.equals(tokens.get(size - 1))) {
                           parsedArgs[1] = tokens.get(size - 2) + " " + tokens.get(size - 1);
                           if ((size - 2) == 1) parsedArgs[0] = tokens.get(0);
                           else parsedArgs[0] = String.join("", tokens.subList(0, size - 2));
                           break;
                       }
                   } else {
                       if (champs.equals(tokens.get(size - 2))) {
                           parsedArgs[1] = tokens.get(size - 3)  + " " + tokens.get(size - 2);
                           if ((size - 3) == 1) parsedArgs[0] = tokens.get(0);
                           else parsedArgs[0] = String.join("", tokens.subList(0, size - 3));
                           break;
                       }

                   }

                }

                if (parsedArgs[1] == null) {
                    if (parsedArgs[2] == null) {
                        parsedArgs[1] = tokens.get(size - 1);
                        if ((size - 1) == 1) parsedArgs[0] = tokens.get(0);
                        else parsedArgs[0] = String.join("", tokens.subList(0, size - 1));
                    } else {
                        parsedArgs[1] = tokens.get(size - 2);
                        if ((size - 2) == 1) parsedArgs[0] = tokens.get(0);
                        else parsedArgs[0] = String.join("", tokens.subList(0, size - 2));
                    }

                }

            } catch (IOException e) {
                LOG.error("Spaces.txt missing for some reason, aborting");
            }

        } else {
            if (parsedArgs[2] == null) {
                parsedArgs[0] = String.join("", tokens.subList(0, size));
            } else {
                parsedArgs[0] = String.join("", tokens.subList(0, size - 1));
            }
        }
        if (parsedArgs[2] == null) {
            try {
                parsedArgs[2] = Region.valueOf(this.db.findEntry(guildID)).getRegion();
            } catch (SQLException e) {
                parsedArgs[2] = null;
            }
        }
        return parsedArgs;
    }
}
