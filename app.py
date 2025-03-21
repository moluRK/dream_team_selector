from flask import Flask, render_template, request
import random

app = Flask(__name__)

# IPL Teams Database:
IPL_Teams = {
    "Chennai Super Kings": {
        "Batsmen": ["Ruturaj Gaikwad","Rachin Ravindra",  "Shivam Dube", "Rahul Tripathi","Deepak Hooda"," Vijay Shankar", "Andre Siddarth","Shaik Rasheed"],
        "Bowlers": ["Matheesha Pathirana", "Noor Ahmed","Khaleel Ahmed","Anshul Kamboj","Nathan Ellis", "Mukesh Choudhary", "Shreyas Gopal","Gurjapneet Singh","KL Nagarkoti"],
        "All-rounders": ["Ravindra Jadeja","Ravichandraran Ashwin","Sam Curran","Jamie Overton","Ramakrishna Ghosh"],
        "Wicket-keepers": ["Deon Conway","MS Dhoni","V Bedi"]
    },
    "Delhi Capitals": {
        "Batsmen": ["KL Rahul", "Tristan Stubbs", "Jake Fraser-McGurk", "Harry Brook","Abhishek Parel","Faf du Plessis","D Ferreira","Karun Nair"],
        "Bowlers": ["Kuldeep Yadav", "Mitchell Starc", "T Natarajan", "Mukesh Kumar", "Mohit Sharma", "PVD Chameera"],
        "All-rounders": ["Axar Patel", "Ashutosh Sharma", "Sameer Rizvi", "Vipraj Nigam", "Madhav Tiwari", "Manvanth Kumar", "Tripurana Vijay", "Darshan Nalkande", "Ajay Mandal"],
        "Wicket-keepers": []
    },
    "Gujarat Titans": {
        "Batsmen": ["Shubman Gill", "JC Buttler", "SE Rutherford", "GD Phillips", "K Kushagra", "Anuj Rawat"],
        "Bowlers": ["Mohammed Siraj", "K Rabada", "M Prasidh Krishna", "G Coetzee", "Gurnoor Brar", "I Sharma", "MJ Suthar","K Khejroliya","Rashid Khan"],
        "All-rounders": ["B Sai Sudharsan", "M Shahrukh Khan", "R Tewatia", "Washington Sundar", "R Sai Kishor","MK Lomror","Arshad Khan","Karim Janat","J Yadav","N Sindu"],
        "Wicket-keepers": []
    },
    "Kolkata Knight Riders": {
        "Batsmen": ["Venktesh Iyer","Rinku Singh",  "Angkrish Raghuvanshi", "Roveman Powell", "Ajinkya Rahane","Manish Pandey"],
        "Bowlers": ["Varun Chakravarthy","Harshit Rana","Spencer Johnson","Vaibhav Arora","Chetan Sakariya","Mayank Markande","Anrich Nortje","Umran malik*"],
        "All-rounders": ["Sunil Narin", "Andre Russel", "Ramandeep Singh", "Moeen Ali","Ankul S Roy"],
        "Wicket-keepers": ["Quinton de Kock","Rahmulla Gurbaaz", "Luvnith Sisodia"]
    },
    "Lucknow Super Giants": {
        "Batsmen": ["RR Pant", "N Pooran", "DA Miller", "AK Markram", "MP Breetzke","Himmat Singh","A Juyal"],
        "Bowlers": ["MP Yadav","Ravi Bishnoi","Avesh Khan","Akash Deep","Mohsin Khan","S Joseph","M Siddharth","DS Rathi","Prince Yadav","Akash Singh",],
        "All-rounders": ["Abdul Samad","A Badoni","MR Marsh","Shahbaz Ahmed","AA Kulkarni","Y Chaudhary","RS Hangargekar"],
        "Wicket-keepers": []
    },
    "Mumbai Indians": {
        "Batsmen": ["Rohit Sharma", "Suryakumar Yadav","Tilak Varma","Rajat Angad Bawa","Bevpon Jacobs"],
        "Bowlers": ["Jasprit Bumrah", "Trent Boult","Deepak Chahar", "Mujeeb-ur-Rahman","Karan Sharma", "Reece Topley", "Ashwani Kumar","Arjun Tendulkar","Vignesh Puthur"],
        "All-rounders": ["Hardik Pandya","Naman Dhir","Will Jacks","Corbin Bosch","Mitchell Santner","S Raju"],
        "Wicket-keepers": ["Ryan Rickelton","KL Shrijith","R Minz"]
    },
    "Punjab Kings": {
        "Batsmen": ["SS Iyer", "N Wadhere","P Avinash","Harnoor Singh","Priyansh Arya"],
        "Bowlers": ["Arshdeep Singh", "YS Chahal", "LH Ferguson", "V Vyshak", "Yash Thakur", "KR Sen","XC Bartlett",],
        "All-rounders": ["Liam Livingstone", "Sam Curran", "Rishi Dhawan", "Raj Bawa", "Atharva Taide"],
        "Wicket-keepers": ["Josh Inglis","Prabhsimram Singh", "Vishnu Vinod"]
    },
    "Rajasthan Royals": {
        "Batsmen": ["Yashasvi Jaiswal","Shimron Hetmyer","Vaiibhav Suryavanshi","Shubham Dubey"],
        "Bowlers": ["Jofra Archer", "Maheesh Theekshana", "Sandeep Sharma","Tushar Deshpande","Akash Madhwal","Fazalhaq Farooqi","Kumar Kartikeya",  "Kwena Maphaka","Ashok Sharma"],
        "All-rounders": [ "Wanindu Hasaranga","Riyan Parag", "Nitish Rana", "Yudhvir Singh Charak"],
        "Wicket-keepers": ["Sanju Samson","DC Jurel","KS Rathod"]
    },
    "Sunrisers Hyderabad": {
        "Batsmen": ["Travish Head", "Kamindu Mendis","Abhinav Manohar", "Aniket VVerma","Atharava Taide","Sachin Baby"],
        "Bowlers": ["Mohammed Shami", "Pat Cummins","Harshal Patel", "Adam Zampa","Rahul Chahar", "Simarjeet Singh", "Eshan Malinga", "Jaydev Unadkat","Zeeshan Ansari"],
        "All-rounders": [ "Abhishek Sharma",  "K Nitish Kumar Reddy", "Wiaan Mulder"],
        "Wicket-keepers": ["Heinrich Klaasen", "Ishan Kishan"]
    },
    "Royal Challengers Bangalore": {
        "Batsmen": ["Virat Kohli", "Rajat Patidar","JG Bethell","D Padikkal","Swastik Chikara","Tim David",],
        "Bowlers": ["Josh Hazlewood","Bhuvneshwar Kumar","Rasikh Salam","Yash Dayal","Suyash Sharma","Nuwan Thushra","L Ngidi","Abhinandan Singh"],
        "All-rounders": ["LS Livingstone", "KH Pandya", "R Shepherd","Swapnil Singh","MS Bhandage","Mohut Rathee"],
        "Wicket-keepers": ["PD Salt", "Jitesh Sharma"]
    }
}

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

        # Ensureing exactly 11 players
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
