from flask import Flask, render_template, request
import random

app = Flask(__name__)

# IPL Teams Database (Make sure all categories exist for every team)
IPL_Teams = {
    "Chennai Super Kings": {
        "Batsmen": ["Ruturaj Gaikwad", "Devon Conway", "Rahul Tripathi", "Shaik Rasheed"],
        "Bowlers": ["Matheesha Pathirana", "Khaleel Ahmed", "Mukesh Choudhary", "Shreyas Gopal"],
        "All-rounders": ["Ravindra Jadeja", "Shivam Dube", "Sam Curran", "Rachin Ravindra"],
        "Wicket-keepers": ["MS Dhoni"]
    },
    "Delhi Capitals": {
        "Batsmen": ["KL Rahul", "Tristan Stubbs", "Jake Fraser-McGurk", "Harry Brook", "Faf du Plessis", "Karun Nair"],
        "Bowlers": ["Kuldeep Yadav", "Mitchell Starc", "T Natarajan", "Mukesh Kumar", "Mohit Sharma", "Dushmantha Chameera"],
        "All-rounders": ["Axar Patel", "Ashutosh Sharma", "Sameer Rizvi", "Vipraj Nigam", "Madhav Tiwari", "Manvanth Kumar", "Tripurana Vijay", "Darshan Nalkande", "Ajay Mandal"],
        "Wicket-keepers": ["Abishek Porel", "Donovan Ferreira"]
    },
    "Gujarat Titans": {
        "Batsmen": ["Shubman Gill", "Kane Williamson", "Sai Sudharsan", "David Miller", "Abhinav Manohar", "Matthew Wade"],
        "Bowlers": ["Mohammed Shami", "Alzarri Joseph", "Yash Dayal", "Pradeep Sangwan", "Rashid Khan", "R Sai Kishore", "Noor Ahmad"],
        "All-rounders": ["Hardik Pandya", "Rahul Tewatia", "Vijay Shankar", "Jayant Yadav", "Odean Smith"],
        "Wicket-keepers": ["Wriddhiman Saha", "Urvil Patel"]
    },
    "Kolkata Knight Riders": {
        "Batsmen": ["Nitish Rana", "Venkatesh Iyer", "Shreyas Iyer", "Rinku Singh", "Mandeep Singh", "Jason Roy"],
        "Bowlers": ["Lockie Ferguson", "Umesh Yadav", "Tim Southee", "Varun Chakravarthy", "Harshit Rana", "Kulwant Khejroliya"],
        "All-rounders": ["Andre Russell", "Sunil Narine", "Shakib Al Hasan", "Anukul Roy", "David Wiese"],
        "Wicket-keepers": ["Rahmanullah Gurbaz", "Litton Das"]
    },
    "Lucknow Super Giants": {
        "Batsmen": ["Manan Vohra", "Deepak Hooda", "Ayush Badoni", "Karan Sharma", "Quinton de Kock"],
        "Bowlers": ["Avesh Khan", "Mark Wood", "Mohsin Khan", "Ravi Bishnoi", "Jaydev Unadkat", "Yash Thakur"],
        "All-rounders": ["Marcus Stoinis", "Krunal Pandya", "Kyle Mayers", "Daniel Sams", "Romario Shepherd"],
        "Wicket-keepers": ["Nicholas Pooran"]
    },
    "Mumbai Indians": {
        "Batsmen": ["Rohit Sharma", "Suryakumar Yadav", "Tilak Varma", "Dewald Brevis", "Ramandeep Singh"],
        "Bowlers": ["Jasprit Bumrah", "Jofra Archer", "Jason Behrendorff", "Piyush Chawla", "Kumar Kartikeya", "Hrithik Shokeen"],
        "All-rounders": ["Cameron Green", "Tim David", "Arjun Tendulkar", "Shams Mulani", "Nehal Wadhera"],
        "Wicket-keepers": ["Ishan Kishan", "Vishnu Vinod"]
    },
    "Punjab Kings": {
        "Batsmen": ["Shikhar Dhawan", "Bhanuka Rajapaksa", "Shahrukh Khan", "Prabhsimran Singh", "Jitesh Sharma"],
        "Bowlers": ["Kagiso Rabada", "Arshdeep Singh", "Rahul Chahar", "Harpreet Brar", "Nathan Ellis", "Baltej Singh"],
        "All-rounders": ["Liam Livingstone", "Sam Curran", "Rishi Dhawan", "Raj Bawa", "Atharva Taide"],
        "Wicket-keepers": []
    },
    "Rajasthan Royals": {
        "Batsmen": ["Sanju Samson", "Jos Buttler", "Yashasvi Jaiswal", "Devdutt Padikkal", "Shimron Hetmyer"],
        "Bowlers": ["Trent Boult", "Prasidh Krishna", "Navdeep Saini", "Kuldeep Sen", "Yuzvendra Chahal", "KC Cariappa"],
        "All-rounders": ["Ravichandran Ashwin", "Riyan Parag", "Jason Holder", "Donovan Ferreira", "Akash Vasisht"],
        "Wicket-keepers": []
    },
    "Sunrisers Hyderabad": {
        "Batsmen": ["Aiden Markram", "Abdul Samad", "Rahul Tripathi", "Mayank Agarwal", "Harry Brook"],
        "Bowlers": ["Bhuvneshwar Kumar", "T Natarajan", "Umran Malik", "Kartik Tyagi", "Adil Rashid", "Mayank Markande"],
        "All-rounders": ["Washington Sundar", "Marco Jansen", "Abhishek Sharma", "Akeal Hosein", "Samarth Vyas"],
        "Wicket-keepers": ["Heinrich Klaasen", "Glenn Phillips"]
    },
    "Royal Challengers Bangalore": {
        "Batsmen": ["Virat Kohli", "Faf du Plessis", "Rajat Patidar", "Anuj Rawat", "Suyash Prabhudessai"],
        "Bowlers": ["Mohammed Siraj", "Harshal Patel", "Josh Hazlewood", "Karn Sharma", "Akash Deep", "Reece Topley"],
        "All-rounders": ["Glenn Maxwell", "Shahbaz Ahmed", "Wanindu Hasaranga", "Michael Bracewell", "Manoj Bhandage"],
        "Wicket-keepers": ["Dinesh Karthik", "Finn Allen"]
    }
}

# Ensure all teams have all categories (even if empty)
for team in IPL_Teams:
    for category in ["Batsmen", "Bowlers", "All-rounders", "Wicketkeepers"]:
        if category not in IPL_Teams[team]:
            IPL_Teams[team][category] = []  # Add empty list if category is missing

def generate_dream_teams(team1, team2, num_teams):
    dream_teams = []
    
    for _ in range(num_teams):
        selected_players = { "Batsmen": [], "Bowlers": [], "All-rounders": [], "Wicketkeepers": [] }
        used_players = set()

        # Function to select players while preventing repetition within the team
        def select_players(category, count):
            available_players = IPL_Teams[team1].get(category, []) + IPL_Teams[team2].get(category, [])
            random.shuffle(available_players)
            selected = []

            for player in available_players:
                if len(selected) >= count:
                    break
                if player not in used_players:
                    selected.append(player)
                    used_players.add(player)
            
            return selected

        # Assign players by category
        selected_players["Batsmen"] = select_players("Batsmen", 3)
        selected_players["Bowlers"] = select_players("Bowlers", 3)
        selected_players["All-rounders"] = select_players("All-rounders", 3)
        selected_players["Wicketkeepers"] = select_players("Wicketkeepers", 2)

        # Ensure exactly 11 players, distributing extra players randomly across categories
        total_selected = sum(len(selected_players[cat]) for cat in selected_players)

        if total_selected < 11:
            all_available = { "Batsmen": [], "Bowlers": [], "All-rounders": [], "Wicketkeepers": [] }
            
            # Collect all available players
            for category in all_available:
                all_available[category] += IPL_Teams[team1].get(category, []) + IPL_Teams[team2].get(category, [])

            # Remove already selected players from available pool
            for category in all_available:
                all_available[category] = [player for player in all_available[category] if player not in used_players]

            # Randomly shuffle category selection to ensure fair distribution
            category_list = ["Batsmen", "Bowlers", "All-rounders", "Wicketkeepers"]
            random.shuffle(category_list)  # Shuffle the order of categories

            while total_selected < 11:
                for category in category_list:
                    if total_selected >= 11:
                        break
                    if all_available[category]:  # If category has available players
                        player = all_available[category].pop(0)  # Take the first available player
                        selected_players[category].append(player)
                        used_players.add(player)
                        total_selected += 1

        # Ensure categories are preserved, even if empty
        for category in selected_players:
            if len(selected_players[category]) == 0:
                selected_players[category] = ["No players available"]

        # Select Captain & Vice Captain
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

    generated_teams = generate_dream_teams(team1, team2, num_teams)

    return render_template('dream_team.html', team1=team1, team2=team2, dream_teams=generated_teams)

if __name__ == '__main__':
    app.run(debug=True)
