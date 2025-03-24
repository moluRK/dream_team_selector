from flask import Flask, render_template, request
import random

app = Flask(__name__)

# IPL_Teams Database (updated to ensure all teams have enough players and wicket-keepers)
IPL_Teams = {
    "Chennai Super Kings": {
        "Batsmen": ["Ruturaj Gaikwad", "Rachin Ravindra", "Shivam Dube", "Rahul Tripathi", "Deepak Hooda", "Vijay Shankar", "Andre Siddarth", "Shaik Rasheed"],
        "Bowlers": ["Matheesha Pathirana", "Noor Ahmed", "Khaleel Ahmed", "Anshul Kamboj", "Nathan Ellis", "Mukesh Choudhary", "Shreyas Gopal", "Gurjapneet Singh", "KL Nagarkoti"],
        "All-rounders": ["Ravindra Jadeja", "Ravichandran Ashwin", "Sam Curran", "Jamie Overton", "Ramakrishna Ghosh"],
        "Wicket-keepers": ["Deon Conway", "MS Dhoni", "V Bedi"]
    },
    "Delhi Capitals": {
        "Batsmen": ["F du Plessis", "Tristan Stubbs", "Jake Fraser-McGurk", "Ashutosh Sharma", "Sameer Rizvi", "Faf du Plessis", "Karun Nair"],
        "Bowlers": ["Kuldeep Yadav", "Mitchell Starc", "T Natarajan", "Dushmanth Chameera", "Mohit Sharma", "M Kumar", "D Nalkande", "T Vijay","V Nigam"],
        "All-rounders": ["Axar Patel", "D Ferreira", "", "A Mandal",  "Manvanth Kumar L", "M Tiwari"],
        "Wicket-keepers": ["KL Rahul","A Porel"]
    },
    "Gujarat Titans": {
        "Batsmen": ["Shubman Gill","G Phillips","S Sudharsan","S Rurherford","M Lomar"],
        "Bowlers": ["Mohammed Siraj", "K Rabada", "Prasidh Krishna", "G Coetzee", "R Sai Kishore", "I Sharma", "J Yadav", "K Khejroliya","G Brar Singh", "Rashid Khan"],
        "All-rounders": ["S Khan, "R Tewatia", "Washington Sundar", "K Janat", "M Suthar", "N Sindhu", "A Khan"],
        "Wicket-keepers": ["J Buttler","A Rawat","K Kushagra"]
    },
    "Kolkata Knight Riders": {
        "Batsmen": ["Venktesh Iyer", "Rinku Singh", "Angkrish Raghuvanshi", "Roveman Powell", "Ajinkya Rahane", "Manish Pandey"],
        "Bowlers": ["Varun Chakravarthy", "Harshit Rana", "Spencer Johnson", "Vaibhav Arora", "Chetan Sakariya", "Mayank Markande", "Anrich Nortje", "Umran Malik"],
        "All-rounders": ["Sunil Narine", "Andre Russell", "Ramandeep Singh", "Moeen Ali", "Ankul S Roy"],
        "Wicket-keepers": ["Quinton de Kock", "Rahmulla Gurbaaz", "Luvnith Sisodia"]
    },
    "Lucknow Super Giants": {
        "Batsmen": ["David Miller", "Mitchell Marsh", "Ayush Badini", "Abdul Samad", "Matthew Breetzke", "Himmat Singh"],
        "Bowlers": ["M Yadav", "Ravi Bishnoi", "Avesh Khan", "Akash Deep", "Mohsin Khan", "S Joseph", "M Siddharth", "S Thakur", "Prince Yadav", "Akash Singh","R Hangargekar","D Singh"],
        "All-rounders": ["Aiden Maekran", "S Ahmed", "A Kulkarni", "Yuvraj Chaudhary"],
        "Wicket-keepers": ["Rishbh Pant","N Pooran","Aryan Juyal"]
    },
    "Mumbai Indians": {
        "Batsmen": ["Rohit Sharma", "Suryakumar Yadav", "Tilak Varma", "Rajat Angad Bawa", "Bevpon Jacobs"],
        "Bowlers": ["Jasprit Bumrah", "Trent Boult", "Deepak Chahar", "Mujeeb-ur-Rahman", "Karan Sharma", "Reece Topley", "Ashwani Kumar", "Arjun Tendulkar", "Vignesh Puthur"],
        "All-rounders": ["Hardik Pandya", "Naman Dhir", "Will Jacks", "Corbin Bosch", "Mitchell Santner", "S Raju"],
        "Wicket-keepers": ["Ryan Rickelton", "KL Shrijith", "R Minz"]
    },
    "Punjab Kings": {
        "Batsmen": ["S Iyer", "N Wadhere", "S Singh", "P Avinash", "Priyansh Arya","H Singh Pannu"],
        "Bowlers": ["Arshdeep Singh", "Y Chahal", "L Ferguson", "V Vijaykumar", "H Brar", "Y Thakur", "XC Bartlett","K Sen","P Dubey"],
        "All-rounders": ["G Maxwell","M Jansen","M Stonis","A Omarzai","A Hardie","M Khan", "S Shedge"],
        "Wicket-keepers": ["Josh Inglis", "Prabhsimran Singh", "Vishnu Vinod"]
    },
    "Rajasthan Royals": {
        "Batsmen": ["Yashasvi Jaiswal", "Shimron Hetmyer", "Vaibhav Suryavanshi", "Shubham Dubey"],
        "Bowlers": ["Jofra Archer", "Maheesh Theekshana", "Sandeep Sharma", "Tushar Deshpande", "Akash Madhwal", "Fazalhaq Farooqi", "Kumar Kartikeya", "Kwena Maphaka", "Ashok Sharma"],
        "All-rounders": ["Wanindu Hasaranga", "Riyan Parag", "Nitish Rana", "Yudhvir Singh Charak"],
        "Wicket-keepers": ["Sanju Samson", "DC Jurel", "KS Rathod"]
    },
    "Sunrisers Hyderabad": {
        "Batsmen": ["Travis Head", "Kamindu Mendis", "Abhinav Manohar", "Aniket VVerma", "Atharva Taide", "Sachin Baby"],
        "Bowlers": ["Mohammed Shami", "Pat Cummins", "Harshal Patel", "Adam Zampa", "Rahul Chahar", "Simarjeet Singh", "Eshan Malinga", "Jaydev Unadkat", "Zeeshan Ansari"],
        "All-rounders": ["Abhishek Sharma", "K Nitish Kumar Reddy", "Wiaan Mulder"],
        "Wicket-keepers": ["Heinrich Klaasen", "Ishan Kishan"]
    },
    "Royal Challengers Bangalore": {
        "Batsmen": ["Virat Kohli", "Rajat Patidar", "JG Bethell", "D Padikkal", "Swastik Chikara", "Tim David"],
        "Bowlers": ["Josh Hazlewood", "Bhuvneshwar Kumar", "Rasikh Salam", "Yash Dayal", "Suyash Sharma", "Nuwan Thushara", "L Ngidi", "Abhinandan Singh"],
        "All-rounders": ["LS Livingstone", "KH Pandya", "R Shepherd", "Swapnil Singh", "MS Bhandage", "Mohut Rathee"],
        "Wicket-keepers": ["PD Salt", "Jitesh Sharma"]
    }
}

def generate_dream_teams(team1, team2, num_teams):
    dream_teams = []

    for _ in range(num_teams):
        selected_players = {"Batsmen": [], "Bowlers": [], "All-rounders": [], "Wicket-keepers": []}
        used_players = set()
        total_selected = 0

        # Ensure at least one Wicket-Keeper is selected
        available_wks = IPL_Teams[team1]["Wicket-keepers"] + IPL_Teams[team2]["Wicket-keepers"]
        if not available_wks:
            return []  # No wicket-keepers available, cannot form a team

        wk = random.choice(available_wks)
        selected_players["Wicket-keepers"].append(wk)
        used_players.add(wk)
        total_selected += 1

        # Function to select players from a category
        def select_players(category, min_count=1, max_count=4):
            nonlocal total_selected
            available = [p for p in (IPL_Teams[team1].get(category, []) + IPL_Teams[team2].get(category, []))
                         if p not in used_players]
            if not available:
                return []
            random.shuffle(available)
            count = random.randint(min_count, min(max_count, len(available)))
            selected = available[:count]
            for p in selected:
                used_players.add(p)
                total_selected += 1
            return selected

        # Select Batsmen, Bowlers, and All-rounders
        selected_players["Batsmen"] = select_players("Batsmen")
        selected_players["Bowlers"] = select_players("Bowlers")
        selected_players["All-rounders"] = select_players("All-rounders")

        # Fill remaining slots to reach 11 players
        all_players = (
            IPL_Teams[team1]["Batsmen"] + IPL_Teams[team2]["Batsmen"] +
            IPL_Teams[team1]["Bowlers"] + IPL_Teams[team2]["Bowlers"] +
            IPL_Teams[team1]["All-rounders"] + IPL_Teams[team2]["All-rounders"] +
            IPL_Teams[team1]["Wicket-keepers"] + IPL_Teams[team2]["Wicket-keepers"]
        )
        remaining = [p for p in all_players if p not in used_players]
        random.shuffle(remaining)

        while total_selected < 11 and remaining:
            player = remaining.pop()
            # Determine the player's category
            if player in IPL_Teams[team1]["Batsmen"] or player in IPL_Teams[team2]["Batsmen"]:
                selected_players["Batsmen"].append(player)
            elif player in IPL_Teams[team1]["Bowlers"] or player in IPL_Teams[team2]["Bowlers"]:
                selected_players["Bowlers"].append(player)
            elif player in IPL_Teams[team1]["All-rounders"] or player in IPL_Teams[team2]["All-rounders"]:
                selected_players["All-rounders"].append(player)
            elif player in IPL_Teams[team1]["Wicket-keepers"] or player in IPL_Teams[team2]["Wicket-keepers"]:
                selected_players["Wicket-keepers"].append(player)
            used_players.add(player)
            total_selected += 1

        # If we still don't have 11 players, skip this team
        if total_selected != 11:
            continue

        # Assign Captain and Vice Captain
        all_players = sum(selected_players.values(), [])
        captain, vice_captain = random.sample(all_players, 2)

        dream_teams.append({
            "players": selected_players,
            "captain": captain,
            "vice_captain": vice_captain
        })

    return dream_teams

@app.route('/')
def home():
    return render_template('index.html', teams=IPL_Teams.keys())

@app.route('/dream-team', methods=['POST'])
def dream_team():
    team1 = request.form.get('team1')
    team2 = request.form.get('team2')
    num_teams = int(request.form.get('num_teams', 1))

    if not team1 or not team2 or num_teams < 1:
        return "Invalid input! Please select teams and a valid number of teams.", 400

    # Check if selected teams have enough players
    total_players = sum(len(IPL_Teams[team1][cat]) for cat in IPL_Teams[team1]) + \
                    sum(len(IPL_Teams[team2][cat]) for cat in IPL_Teams[team2])
    if total_players < 11:
        return "Selected teams don't have enough players to form a team.", 400

    # Check if at least one wicket-keeper is available
    wk_available = IPL_Teams[team1]["Wicket-keepers"] + IPL_Teams[team2]["Wicket-keepers"]
    if not wk_available:
        return "No wicket-keepers available in selected teams. Please choose different teams.", 400

    generated_teams = generate_dream_teams(team1, team2, num_teams)
    if not generated_teams:
        return "Failed to generate teams due to insufficient players.", 500

    return render_template('dream_team.html', team1=team1, team2=team2, dream_teams=generated_teams)

if __name__ == '__main__':
    app.run(debug=True)
