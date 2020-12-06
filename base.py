def whole():
    ###############################################################################
    #################################### Setup ####################################
    ############ Imports pandas and creates simple variables for reuse ############
    
    # imports pandas for DataFrame use
    import pandas as pd
    
    # imports pulp for linear programming use
    import pulp
    
    # variables declared for week and year number for reuse throughout code
    week_num = 13
    year_num = 20
    
    #################################### Setup ####################################
    ###############################################################################
    ############################### Step 1: Creation ##############################
    ### Creates DataFrames for projections and salaries by reading in csvs/urls ###
    
    # reads in csv of salaries and transfers data to DataFrame
    def create_salaries_df(df):
        # creates file path
        file = (r"C:\Users\ben_m\OneDrive\Documents\NFL\\" + str(year_num) + "-"
                + str(year_num + 1) + "CSVs\\" + str(year_num) + "-"
                + str(year_num + 1) + "Week" + str(week_num) + "FD.csv")
        
        # creates table of file path data
        raw_df = pd.read_csv(file)
        
        # creates DataFrame off of raw table data
        df = pd.DataFrame(raw_df)
        
        # returns DataFrame
        return df
        
    # initializes salaries DataFrame
    salaries = pd.DataFrame()
    
    # calls create_salaries_df(df) method to obtain base salaries DataFrame
    salaries = create_salaries_df(salaries)
    
    # reads in fantasy pros projections and transfers data to DataFrame 
    def create_projection_df(df, pos):
        # creates url path
        url = ("https://www.fantasypros.com/nfl/projections/" + pos + ".php")
    
        # creates table out of url data
        raw_df = pd.read_html(url)[0]
        
        # creates DataFrame off of raw table data
        df = pd.DataFrame(raw_df)
        
        #returns DataFrame
        return df
        
    # initializes projections DataFrames
    projections_qb = pd.DataFrame()
    projections_rb = pd.DataFrame()
    projections_wr = pd.DataFrame()
    projections_te = pd.DataFrame()
    projections_dst = pd.DataFrame()
    
    # calls create_projection_df(df, pos) method to obtain base DataFrames for each
    # position
    projections_qb = create_projection_df(projections_qb, "qb")
    projections_rb = create_projection_df(projections_rb, "rb")
    projections_wr = create_projection_df(projections_wr, "wr")
    projections_te = create_projection_df(projections_te, "te")
    projections_dst = create_projection_df(projections_dst, "dst")
    
    ############################### Step 1: Creation ##############################
    ###############################################################################
    ############################# Step 2: Orginization ############################
    ################ Organizes projections and salaries DataFrames ################
    
    # organizes the salaries DataFrame
    def organize_salaries(df):
        # merges first and last name columns
        df["Name"] = df["First Name"].str.cat(df["Last Name"], sep=" ")
        
        # drops columns that are not needed
        df = df.drop(columns = ["Id", "Nickname", "FPPG", "Played", "Tier",
                                "First Name", "Last Name", "Game",
                                "Injury Details"], axis = 1)
        
        # renames Injury Indicator column
        df = df.rename(columns = {"Injury Indicator": "Injury"})
        
        # changes the order of columns in order of importance
        df = df[["Name", "Position", "Salary", "Team", "Opponent", "Injury"]]
        
        # returns organized Dataframe
        return df
    
    # calls organize_salaries(df) method to organize the salaries DataFrame
    salaries = organize_salaries(salaries)
    
    # organizes the projections DataFrames
    def organize_projections(df, pos):
        # gets rid of multi_indexed columns(dst doesn't have this problem)
        if (pos != "dst"):
            df.columns = df.columns.droplevel(0)
    
        # renames columns(columns are position-specific)
        if (pos == "qb"):
            df.columns = ["Name", "Pass Att", "Pass Cmp", "Pass Yds", "Pass TDs",
                          "Ints", "Rush Att", "Rush Yds", "Rush TDs", "FL", "FPTS"]
        elif (pos == "rb"):
            df.columns = ["Name", "Rush Att", "Rush Yds", "Rush TDs", "Recs",
                          "Rec Yds", "Rec TDs", "FL", "FPTS"]
        elif (pos == "wr"):
            df.columns = ["Name", "Recs", "Rec Yds", "Rec TDs", "Rush Att",
                          "Rush Yds", "Rush TDs", "FL", "FPTS"]
        elif (pos == "te"):
            df.columns = ["Name", "Recs", "Rec Yds", "Rec TDs", "FL", "FPTS"]
        else:
            df.columns = ["Name","Sacks","Ints","FR","FF","TDs","Safety","PA",
                          "YA","FPTS"]
        
        # gets rid of team name after player name and adds it to team name column
        # (dst must be handled differently)
        if (pos != "dst"):
            # inserts team name column for each player
            df.insert(1, "Team", "")
            
            # iterates through each row in name column
            for index, row in df.iterrows():
                
                # finds last index of a space in the name
                cutoff = row["Name"].rindex(" ")
                
                # fills team name column with team initials
                df.at[index, "Team"] = row["Name"][cutoff + 1:]
                
                # removes the part following and including the last space
                df.at[index, "Name"] = row["Name"][0: cutoff]
        else:
            # dictionary of initials for each defense's team
            dst_team_names = {"Arizona Cardinals" : "ARI",
                              "Atlanta Falcons" : "ATL",
                              "Baltimore Ravens" : "BAL",
                              "Buffalo Bills" : "BUF",
                              "Carolina Panthers" : "CAR",
                              "Chicago Bears" : "CHI",
                              "Cincinnati Bengals" : "CIN",
                              "Cleveland Browns" : "CLE",
                              "Dallas Cowboys" : "DAL",
                              "Denver Broncos" : "DEN",
                              "Detroit Lions" : "DET",
                              "Green Bay Packers" : "GB",
                              "Houston Texans" : "HOU",
                              "Indianapolis Colts" : "IND",
                              "Jacksonville Jaguars" : "JAC",
                              "Kansas City Chiefs" : "KC",
                              "Los Angeles Chargers" : "LAC",
                              "Los Angeles Rams" : "LAR",
                              "Las Vegas Raiders" : "LV",
                              "Miami Dolphins" : "MIA",
                              "Minnesota Vikings" : "MIN",
                              "New England Patriots" : "NE",
                              "New Orleans Saints" : "NO",
                              "New York Giants" : "NYG",
                              "New York Jets" : "NYJ",
                              "Philadelphia Eagles" : "PHI",
                              "Pittsburgh Steelers" : "PIT",
                              "San Francisco 49ers" : "SF",
                              "Seattle Seahawks" : "SEA",
                              "Tampa Bay Buccaneers" : "TB",
                              "Tennessee Titans" : "TEN",
                              "Washington Redskins" : "WAS"}
            
            # inserts team name column for each defense
            df.insert(1, "Team", "")
            
            # iterates through each row in name column
            for index, row in df.iterrows():
            
                # sets team name to corrected initials
                df.at[index, "Team"] = dst_team_names.get(df.at[index, "Name"])
            
        # returns organized DataFrame
        return df
    
    # calls organize_projetions(df) method to organize the salaries DataFrame
    projections_qb = organize_projections(projections_qb, "qb")
    projections_rb = organize_projections(projections_rb, "rb")
    projections_wr = organize_projections(projections_wr, "wr")
    projections_te = organize_projections(projections_te, "te")
    projections_dst = organize_projections(projections_dst, "dst")
            
    ############################# Step 2: Orginization ############################
    ###############################################################################
    ############################# Step 3: Calculation #############################
    ## Calculates projected points for each position and sets those values to a ###
    #################### newly created projected points column ####################
    
    # creates and sets the projected points column
    def create_projected_points(df, pos):
        # adds projected points column
        df.insert(1, "Projected", 0)
        
        # fills projected points column as a function of player's projected stats
        if (pos == "qb"):
            df["Projected"] = ((df["Pass Yds"] * .04) + (df["Pass TDs"] * 4)
                               - (df["Ints"] * 1) + (df["Rush Yds"] * .1)
                               + (df["Rush TDs"] * 6) - (df["FL"] * .2))
        elif (pos == "rb"):
            df["Projected"] = ((df["Rush Yds"] * .1) + (df["Rush TDs"] * 6)
                               + (df["Recs"] * .5) + (df["Rec Yds"] * .1)
                               + (df["Rec TDs"] * 6) - (df["FL"] * 2))
        elif (pos == "wr"):
            df["Projected"] = ((df["Recs"] * .5) + (df["Rec Yds"] * .1)
                               + (df["Rec TDs"] * 6) + (df["Rush Yds"] * .1)
                               + (df["Rush TDs"] * 6) - (df["FL"] * 2))
        elif (pos == "te"):
            df["Projected"] = ((df["Recs"] * .5) + (df["Rec Yds"] * .1) 
                               + (df["Rec TDs"] * 6) - (df["FL"] * 2))
        else:
            # calls points_against(df) to finish point calculation
            df = points_against(df)
            df["Projected"] = ((df["Sacks"] * 1) + (df["Ints"] * 2)
                               + (df["FR"] * 2)  + (df["TDs"] * 6)
                               + (df["Safety"] * 2) + df["Temp"])
            
            # removes dummy column once it is done being used
            df = df.drop(columns = "Temp")
            
        # rounds the projected points to the 2nd decimal place
        df["Projected"] = round(df["Projected"], 3)
        
        # returns DataFrame with added projected points column
        return df
    
    # calculates the projected points for points against for defenses
    def points_against(df):
        # adds dummy column
        df.insert(1, "Temp", 0)
        
        # creates dummy value to hold the projected points
        value = 0
        
        # iterates through each row of points against column
        for index, row in df.iterrows():
                # sets value according to points against
                if (df.at[index, "PA"] <= 0):
                    value = 10
                elif (df.at[index, "PA"] > 0 and df.at[index, "PA"] < 7):
                    value = 7
                elif (df.at[index, "PA"] > 6 and df.at[index, "PA"] < 14):
                    value =  4
                elif (df.at[index, "PA"] > 13 and df.at[index, "PA"] < 21):
                    value = 1
                elif (df.at[index, "PA"] > 20 and df.at[index, "PA"] < 28):
                    value = 0
                elif (df.at[index, "PA"] > 27 and df.at[index, "PA"] < 35):
                    value = -1
                else:
                    value = -4
                    
                # fills dummy column with values for each row
                df.at[index, "Temp"] = value
                
        # returns DataFrame with dummy column
        return df
    
    # calls create_projected_points method to add projected points into DataFrame
    projections_qb = create_projected_points(projections_qb, "qb")
    projections_rb = create_projected_points(projections_rb, "rb")
    projections_wr = create_projected_points(projections_wr, "wr")
    projections_te = create_projected_points(projections_te, "te")
    projections_dst = create_projected_points(projections_dst, "dst")
    
    #################################### Step 3 ###################################
    ###############################################################################
    ############################# Step 4: Modification ############################
    #### Modifies names(FP -> FD) with the use of a name change dictionary and ####
    ######### removes players that are listed twice in the wrong position #########
    
    # the holy bible of name modifications
    holy_bible = {"Allen Robinson" : "Allen Robinson II",
                  "Bruce Anderson" : "Bruce Anderson III",
                  "CJ Ham" : "C.J. Ham",
                  "Chris Herndon IV" : "Chris Herndon",
                  "D.J. Chark" : "DJ Chark Jr.",
                  "D.J. Moore" : "DJ Moore",
                  "D.K. Metcalf" : "DK Metcalf",
                  "Darrell Henderson" : "Darrell Henderson Jr.",
                  "Darvin Kidsy" : "Darvin Kidsy Jr.",
                  "Donald Parham" : "Donald Parham Jr.",
                  "Dwayne Haskins" : "Dwayne Haskins Jr.",
                  "Gary Jennings Jr." : "Gary Jennings",
                  "J.J. Arcega-Whiteside" : "JJ Arcega-Whiteside",
                  "Jeff Wilson" : "Jeff Wilson Jr.",
                  "John Ross" : "John Ross III",
                  "Karan Higdon" : "Karan Higdon Jr.",
                  "Marvin Jones" : "Marvin Jones Jr.",
                  "Melvin Gordon" : "Melvin Gordon III",
                  "Mitch Trubisky" : "Mitchell Trubisky",
                  "Phillip Dorsett" : "Phillip Dorsett II",
                  "Robert Griffin" : "Robert Griffin III",
                  "Stanley Morgan Jr." : "Stanley Morgan",
                  "Steven Sims" : "Steven Sims Jr.",
                  "Tedd Ginn" : "Tedd Ginn Jr.",
                  "Todd Gurley" : "Todd Gurley II",
                  "Wayne Gallman" : "Wayne Gallman Jr.",
                  "Will Fuller" : "Will Fuller V",
                  "Willie Snead" : "Willie Snead IV"}
    
    # modifies the names of the projections DataFrame to match with salaries
    def modify_names(df, pos):
        # iterates through each row of the name column
        for index, row in df.iterrows():
            # sets name to corrected name if it is in dictionary
            df.at[index, "Name"] = holy_bible.get(df.at[index, "Name"],
                                                  df.at[index, "Name"])
            
        # returns name-corrected DataFrame
        return df
            
    # calls modify_name(df, pos) method to change names to math with salaries
    projections_qb = modify_names(projections_qb, "qb")
    projections_rb = modify_names(projections_rb, "rb")
    projections_wr = modify_names(projections_wr, "wr")
    projections_te = modify_names(projections_te, "te")
    projections_dst = modify_names(projections_dst, "dst")
    
    ############################# Step 4: Modification ############################
    ###############################################################################
    ############################## Step 5: Integration ############################
    ### Integrates projections and salaries to create a new DataFrame with only ###
    ## columns for name, projected points, position, salary, team name, and teir ##
    
    # creates final DataFrame for use in optimization
    def create_final_df(df1, df2, df3, df4, df5, df6):
        # combines name columns of all projection DataFrames into a table
        combo_names = [df1["Name"], df2["Name"], df3["Name"], df4["Name"],
                       df5["Name"]]
        
        # puts all the names in one column
        combo_names = pd.concat(combo_names)
        
        # combines projected points columns of all projection DataFrames into a
        # table
        combo_projected_points = [df1["Projected"], df2["Projected"],
                                  df3["Projected"], df4["Projected"],
                                  df5["Projected"]]
        
        # puts all the projected points in one column
        combo_projected_points = pd.concat(combo_projected_points)
        
        # adds dummy columns for position for each projection DataFrame and sets
        # the correspoding value to the correct position
        df1.insert(1, "Position", "qb")
        df2.insert(1, "Position", "rb")
        df3.insert(1, "Position", "wr")
        df4.insert(1, "Position", "te")
        df5.insert(1, "Position", "dst")
        
        # combines team name columns of all projection DataFrames into a table
        combo_team_name = [df1["Team"], df2["Team"], df3["Team"], df4["Team"],
                           df5["Team"]]
        
        # puts all the team names in one column
        combo_team_name= pd.concat(combo_team_name)
        
        # initialized combo of all columns DataFrame(except salary and position)
        combo = pd.DataFrame(columns = ["Name", "Projected Points", "Team"])
        
        # sets each of the final DataFrame's columns to the combination of all
        # names, projected points, and team name
        combo["Name"] = combo_names
        combo["Projected Points"] = combo_projected_points
        combo["Team"] = combo_team_name
        
        # creates a DataFrame with columns: name and salary
        combo_salaries = pd.DataFrame(columns = ["Name", "Salary"])
        
        # sets the columns of this new DataFrame to the name and salary columns of
        # salaries
        combo_salaries["Name"] = df6["Name"]
        combo_salaries["Salary"] = df6["Salary"]
        
        # merges the newly created DataFrame with the final DataFrame to include
        # salaries with their correct players and simulateously deletes players
        # that have a salary of NaN
        combo = pd.merge(combo, combo_salaries, on = "Name")
        
        # creates a DataFrame with columns: name and position
        combo_positions = pd.DataFrame(columns = ["Name", "Position"])
        
        # sets the columns of this new DataFrame to the name and position columns
        # of salaries
        combo_positions["Name"] = df6["Name"]
        combo_positions["Position"] = df6["Position"]
        
        # merges the newly created DataFrame with the final DataFrame to include
        # positions with their correct players
        combo = pd.merge(combo, combo_positions, on = "Name")
        
        # removes all players with a projected points or salary value of 0
        combo = combo[(combo != 0).all(1)]
        
        # sorts the final DataFrame by salary(high to low)
        combo = combo.sort_values(by=["Salary"], ascending = False)
        
        # creates new tier column for added data
        combo.insert(4, "Tier", "")
        
        # iterates through each row in the final DataFrame
        for index, row in combo.iterrows():
            # sets projected points / salary as a variable
            value = combo.at[index, "Projected Points"] / combo.at[index, "Salary"]
            
            # creates variable for diving by total salary to get tier values
            divisor = 60000
            
            # sets tier column
            if (combo.at[index, "Position"] == "QB"):
                # sets the tier column based on projected points / salary ratio(value)
                # for qbs
                if (value > (180 / divisor)):
                    combo.at[index, "Tier"] = "S"
                elif (value > (175 / divisor)):
                    combo.at[index, "Tier"] = "A+"
                elif (value > (170 / divisor)):
                    combo.at[index, "Tier"] = "A"
                elif (value > (165 / divisor)):
                    combo.at[index, "Tier"] = "A-"
                elif (value > (160 / divisor)):
                    combo.at[index, "Tier"] = "B+"
                elif (value > (155 / divisor)):
                    combo.at[index, "Tier"] = "B"
                elif (value > (150 / divisor)):
                    combo.at[index, "Tier"] = "B-"
                elif (value > (145 / divisor)):
                    combo.at[index, "Tier"] = "C+"
                elif (value > (140 / divisor)):
                    combo.at[index, "Tier"] = "C"
                elif (value > (135 / divisor)):
                    combo.at[index, "Tier"] = "C-"
                elif (value > (130 / divisor)):
                    combo.at[index, "Tier"] = "D+"
                elif (value > (125 / divisor)):
                    combo.at[index, "Tier"] = "D"
                elif (value > (120 / divisor)):
                    combo.at[index, "Tier"] = "D-"
                else:
                    combo.at[index, "Tier"] = "F"
            else:
                # sets the tier column based on projected points / salary ratio(value)
                # for every other position but qb
                if (value > (145 / divisor)):
                    combo.at[index, "Tier"] = "S"
                elif (value > (140 / divisor)):
                    combo.at[index, "Tier"] = "A+"
                elif (value > (135 / divisor)):
                    combo.at[index, "Tier"] = "A"
                elif (value > (130 / divisor)):
                    combo.at[index, "Tier"] = "A-"
                elif (value > (125 / divisor)):
                    combo.at[index, "Tier"] = "B+"
                elif (value > (120 / divisor)):
                    combo.at[index, "Tier"] = "B"
                elif (value > (115 / divisor)):
                    combo.at[index, "Tier"] = "B-"
                elif (value > (110 / divisor)):
                    combo.at[index, "Tier"] = "C+"
                elif (value > (105 / divisor)):
                    combo.at[index, "Tier"] = "C"
                elif (value > (100 / divisor)):
                    combo.at[index, "Tier"] = "C-"
                elif (value > (95 / divisor)):
                    combo.at[index, "Tier"] = "D+"
                elif (value > (90 / divisor)):
                    combo.at[index, "Tier"] = "D"
                elif (value > (85 / divisor)):
                    combo.at[index, "Tier"] = "D-"
                else:
                    combo.at[index, "Tier"] = "F"
                    
                # drops duplicated players to only keep one of them
                combo_temp = combo.drop_duplicates(subset = ["Name"],
                                                   keep = "first", inplace = False)
                
                # dictionary and duplicated players correct positions
                position_change = {"A.J. Green" : "WR",
                                   "Taysom Hill" : "QB"}
                
                # manually fixing their positions
                for index, row in combo_temp.iterrows():
                    combo_temp.at[index, "Position"] = position_change.get(
                        combo_temp.at[index, "Name"],
                        combo_temp.at[index, "Position"])
                    
        # returns the final DataFrame
        return combo_temp
    
    # initializes final DataFrame
    final = pd.DataFrame()
    
    # calls create_final_df(df, df2, df3, df4, df5, df6, df7) to create final
    # DataFrame
    final = create_final_df(projections_qb, projections_rb, projections_wr,
                            projections_te, projections_dst, salaries)
    
    ############################## Step 5: Integration ############################
    ###############################################################################
    ############################# Step 6: Optimization ############################
    ## Optimizes the final DataFrame for the best possible lineup with a salary ###
    ################################## of $60000 ##################################
    
    # optimizes and creates final lineup
    def get_lineup(df, player_number_constraint, salary_constraint,
                   qb_number_constraint, rb_number_constraint,
                   wr_number_constraint, te_number_constraint,
                   dst_number_constraint, team_number_constraint,
                   projected_points_constraint):
        # creates deep copy of final DataFrame to make temporary changes for use in
        # lp problem
        temp = df.copy(deep = True)
        
        # adds columns for each position that will be filled with 0s and 1s for
        # constraints in lp
        temp.insert(1, "qb", 0)
        temp.insert(1, "rb", 0)
        temp.insert(1, "wr", 0)
        temp.insert(1, "te", 0)
        temp.insert(1, "dst", 0)
        
        # fills each position specific row with a 1 if the player is of that
        # positions and 0 otherwise
        for index, row in temp.iterrows():
            if (temp.at[index, "Position"] == "QB"):
                temp.at[index, "qb"] = 1
            elif (temp.at[index, "Position"] == "RB"):
                temp.at[index, "rb"] = 1
            elif (temp.at[index, "Position"] == "WR"):
                temp.at[index, "wr"] = 1
            elif (temp.at[index, "Position"] == "TE"):
                temp.at[index, "te"] = 1
            else:
                temp.at[index, "dst"] = 1
        
        # organizes the final DataFrame so name of player is index rather than
        # integer
        temp.set_index("Name", inplace = True)
                
        # creates dictionary of player names from passed in DataFrame
        players = temp.index.tolist()
        
        # creates dictionaries of each important variable for players for use in
        # lp problem
        player_projections = temp["Projected Points"].to_dict() 
        player_salaries = temp["Salary"].to_dict()
        player_positions = temp["Position"].to_dict()
        player_teams = temp["Team"].to_dict()
        player_tiers = temp["Tier"].to_dict()
        player_qb = temp["qb"].to_dict()
        player_rb = temp["rb"].to_dict()
        player_wr = temp["wr"].to_dict()
        player_te = temp["te"].to_dict()
        player_dst = temp["dst"].to_dict()
        
        # initializes lp problem
        lp_problem = pulp.LpProblem("Optimize Lineup", pulp.LpMaximize)
        
        # creates list of binary integers(0 or 1) where 1 means a player is chosen
        # in the final lineup and 0 otherwise
        player_selection_binary = pulp.LpVariable.dicts("Choose", players, 0,
                                                        cat ='Binary')
        
        ###########################################################################
        #  For all constraints, columns with numbers are used and multiplied by   #
        #     the player_selection_binary column to make sure that no single      #
        #  constraint is broken. For example, the salary column is multiplied by  #
        #  the psb column where only players that have 1s in psb(have met every   #
        #  other constraint so far and are still in the final lineup as of then)  #
        # will have their salaries count towards making a lineup that follows the #
        # total salary constraint, and every other player with a 0 will not have  #
        #             their salary affect the constraint calculation              #
        ###########################################################################
        
        # sets objective function of lp problem to maximize the total projected
        # points of all the players chosen to be in the final lineup
        lp_problem += (pulp.lpSum([player_projections[i] *
                                   player_selection_binary[i] for i in players]))
        
        # sets player number constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_selection_binary[i] for i in players])
                                   == player_number_constraint)
                
        # sets salary constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_salaries[i] * player_selection_binary[i]
                                   for i in players]) <= salary_constraint)
        
        # sets qb number constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_qb[i] * player_selection_binary[i]
                                   for i in players]) == qb_number_constraint)
       
        # sets rb number constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_rb[i] * player_selection_binary[i]
                                   for i in players]) >= rb_number_constraint)
        
        # sets wr number constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_wr[i] * player_selection_binary[i]
                                   for i in players]) >= wr_number_constraint)
        
        # sets te number constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_te[i] * player_selection_binary[i]
                                   for i in players]) >= te_number_constraint)
        # sets dst number constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_dst[i] * player_selection_binary[i]
                                   for i in players]) == dst_number_constraint)
        
        # sets team number constraint to be whatever is passed in by looping
        # every team
        for team in player_teams:
            lp_problem += (pulp.lpSum([player_selection_binary[j] for j, k in 
                           zip(players, player_teams) if k == team])
                           <= team_number_constraint)
            
        # sets projected points constraint to be whatever is passed in
        lp_problem += (pulp.lpSum([player_projections[i] *
                                   player_selection_binary[i] for i in players])
                                   <= projected_points_constraint)
        
        # solves the lp problem
        lp_problem.solve()
    
        # the list of items in the player_selection_binary list of players
        player_selection = {v: k for k, v in player_selection_binary.items()}
        
        # initializes total projection, total salary, and final lineup
        total_projection = 0
        total_salary = 0
        lineup = {}
        
        # iterates through evey item in the columns of every lp variable
        for v in lp_problem.variables():
            # if the player was chosen then their data is recorded and added to the
            # total, projection, total salary, and final lineup
            if v.varValue == 1 and "Choose" in v.name:
                lineup_player_name = player_selection[v]
                lineup_player_salary = player_salaries[lineup_player_name]
                lineup_player_projection = player_projections[lineup_player_name]
                lineup_player_position = player_positions[lineup_player_name]
                lineup_player_team = player_teams[lineup_player_name]
                lineup_player_tier = player_tiers[lineup_player_name]
                total_projection += lineup_player_projection
                total_salary += lineup_player_salary
                lineup[lineup_player_name] = [lineup_player_salary,
                                       lineup_player_projection,
                                       lineup_player_position, lineup_player_team,
                                       lineup_player_tier]
        
        # assigns the tier for the total lineup based on the same levels used
        # before
        if (total_projection > 150):
            insert = "S"
        elif (total_projection > 145):
            insert = "A+"
        elif (total_projection > 140):
            insert = "A"
        elif (total_projection > 135):
            insert = "A-"
        elif (total_projection > 130):
            insert = "B+"
        elif (total_projection > 125):
            insert = "B"
        elif (total_projection > 120):
            insert = "B-"
        elif (total_projection > 115):
            insert = "C+"
        elif (total_projection > 110):
            insert = "C"
        elif (total_projection > 105):
            insert = "C-"
        elif (total_projection > 100):
            insert = "D+"
        elif (total_projection > 95):
            insert = "D"
        elif (total_projection > 90):
            insert = "D-"
        else:
            insert = "F"      
                
        # adds a total row with all the values combined
        lineup["Total"] = [total_salary, total_projection, None, None, insert]
        
        # a DataFrame is created out of the final lineup for manipulation
        lineupDF = pd.DataFrame(lineup)
        
        # axes are switched so that players names are now the indexes
        lineupDF = lineupDF.T
        
        # the columns are named to their respective names
        lineupDF.columns = ["Salary", "Projected Points", "Position", "Team",
                            "Tier"]
        
        # sorts by projected points first so higher projected players of the same
        # position will be listed first
        lineupDF = lineupDF.sort_values("Projected Points", ascending = False)
        
        # maps the order of positions that we want to be sorted in the lineup
        map_positions = {"QB" : 1, "RB" : 2, "WR" : 3, "TE" : 4, "D" : 5}
        
        # creates a dummy column to be sorted by with the newly created order
        lineupDF["Mapped Positions"] = lineupDF["Position"].map(map_positions)
        
        # sorts the lineup by the dummy column
        lineupDF = lineupDF.sort_values("Mapped Positions", ascending = True)
        
        # drops dummy column that was used for sorting
        lineupDF = lineupDF.drop(columns = ["Mapped Positions"])
        
        # rounds the projection column for total to the second decimal place
        lineupDF.at["Total", "Projected Points"] = round(lineupDF.at[
            "Total","Projected Points"], 3)
        
        # the final lineup is returned
        return lineupDF
    
    # calls the get_lineup method to obtain the optimized lineup with each specific
    # paramater passed in([final] for final data use, [9] for player number
    # constraint, [60000] for salary constraint, [1] for qb number constraint, [2]
    # for rb number constraint, [3] for wr number constraint, [1] for te number
    # constraint, [1] for dst number constraint, [5] for team number constraint,
    # and [999999] to for projection constraint)
    optimized_lineup = get_lineup(final, 9, 60000, 1, 2, 3, 1, 1, 5, 999999)
    
    # creates top constraint for projected points to get 2nd best lineup(pulp does
    # not allow strictly < operators so I have to use <= and therefore have to make
    # the boundary a little smaller than actuality)
    most_points = (optimized_lineup.at["Total", "Projected Points"] - .001)
    
    # creates second best lineup
    optimized_lineup_2 = get_lineup(final, 9, 60000, 1, 2, 3, 1, 1, 5, most_points)
    
    # sets top constraint for projected points to get 3rd best lineup
    most_points = (optimized_lineup_2.at["Total", "Projected Points"] - .001)
    
    # creates 3rd best lineup
    optimized_lineup_3 = get_lineup(final, 9, 60000, 1, 2, 3, 1, 1, 5, most_points)
    
    # returns the lineups
    return optimized_lineup, optimized_lineup_2, optimized_lineup_3
    ############################# Step 6: Optimization ############################
    ###############################################################################