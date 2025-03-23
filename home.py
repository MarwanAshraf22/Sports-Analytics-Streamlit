import streamlit as st
from PIL import Image
import pandas as pd

# Load images
stadium_image = Image.open('images/stadium.jpg')
players_image = Image.open('images/legends.jpg')
trophy_image = Image.open('images/trophies.jpg')

def display_home():
    # History of Real Madrid CF
    st.markdown('<div class="subheader">History of Real Madrid CF</div>', unsafe_allow_html=True)
    st.write("""**Real Madrid Club de Fútbol** is a legendary football club based in Madrid, Spain, founded in **1902**. The club has grown into one of the most successful and prestigious in the world, known for its success both in Spain and internationally.""")

    # Display Stadium Image
    st.image(stadium_image, caption="Santiago Bernabéu Stadium", use_container_width=True)

    # Club Legends
    st.write("""Real Madrid has been home to some of the best footballers ever, including:
    - **Alfredo Di Stéfano**: The Argentine legend who led Real Madrid to five consecutive European Cup titles.
    - **Cristiano Ronaldo**: The Portuguese forward who broke countless records and became the club's all-time top scorer.
    - **Zinedine Zidane**: The French maestro who not only won titles but also led the club to three consecutive UEFA Champions League victories as a manager.
    """)

    # Resize Legends Image
    players_image_resized = players_image.resize((players_image.width, 400))  # Adjust height to 400px
    st.image(players_image_resized, caption="Real Madrid Legends", use_container_width=True)

    # Achievements Table
    achievements_data = {
        'Title': ['La Liga Titles', 'UEFA Champions League Titles', 'Copa del Rey Titles', 
                  'Supercopa de España Titles', 'UEFA Super Cups', 'UEFA Cups', 
                  'Intercontinental Cups', 'FIFA Club World Cups', 'Copa Eva Duarte', 
                  'Copa de la Liga', 'Latin Cups', 'Copa Iberoamericana'],
        'Number of Titles': [36, 15, 20, 13, 6, 2, 3, 5, 1, 1, 2, 1]
    }
    df = pd.DataFrame(achievements_data)

    st.markdown('<div class="subheader">Achievements</div>', unsafe_allow_html=True)
    st.table(df)

    # Resize Trophy Image
    trophy_image_resized = trophy_image.resize((trophy_image.width, 1000))  # Adjust height to 400px
    st.image(trophy_image_resized, caption="Real Madrid Trophies", use_container_width=True)

    # Global Phenomenon Section
    st.markdown('<div class="subheader">Real Madrid: A Global Phenomenon</div>', unsafe_allow_html=True)
    st.write("""Real Madrid is not only famous for its history and achievements but also for its massive global following. 
    With millions of fans from every corner of the globe, the club has established an unmatched legacy in the footballing world.
    The club’s fanbase, known as **Los Blancos**, is one of the most passionate and loyal groups of supporters.
    """)

    # Embed YouTube Video
    st.markdown('<div class="subheader">Watch Real Madrid’s Story</div>', unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=ctm_eJ6wcGs&ab_channel=GoalZone")
