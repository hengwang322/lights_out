import os
from PIL import Image

import streamlit as st
import pandas as pd
import plotly.express as px

from src.plot import plot_cost, plot_lighting_map, plot_lamp_hist, plot_solar

MAPBOX_TOKEN = os.environ['MAPBOX_TOKEN']


def update_style():
    BACKGROUND_COLOR = "rgb(50,50,50)"
    COLOR = "#fff"

    st.markdown(
        f"""
        <style>
            .reportview-container .main {{
                color: {COLOR};
                background-color: {BACKGROUND_COLOR};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <style>
            .reportview-container .main {{
                color: {COLOR};
                background-color: {BACKGROUND_COLOR};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def df_float_formatter(df, formatter="{:.2f}"):
    """Select float columns and format them with formatter."""
    float_col = df.select_dtypes(include='float64').columns
    format_dict = {col: formatter for col in float_col}
    df = df.style.format(format_dict)
    return df


def main():
    st.set_page_config(page_title='Lights Out!',
                            page_icon="💡",
                            initial_sidebar_state='collapsed')
    update_style()

    st.markdown("""<h1 style="text-align:center">Lights Out!</h1>""",
                unsafe_allow_html=True)

    st.markdown(
        """
        <p style="text-align:justify">Street lighting comprises of 14.8% (9,935 GJ)
         of total energy used by the City of Hobart, and is a major contributor 
         to electrical and greenhouse gas usage in all cities. The City of Hobart 
         spends approximately $1.5 - $2 million dollars a year and would like to 
         investigate strategies to reduce their energy costs and light pollution.</p>
        <p style="text-align:justify">There are over 5,000 street lights in the City 
        of Hobart, where only 300 are managed by the city. The rest of the lights are 
        managed by TasNetworks and are unmetered. This means regardless if the light 
        is on, off, or dimmed, the council pays the full 10 hours a day.</p>
        <p style="text-align:justify">We wanted to investigate 4 main ideas:</p>
        <li>Which bulbs are the most effective, and is it cost-effective to swap bulbs?</li>
        <li>Is it worth metering individual poles to reduce electricity costs from 
        dimming with and without sensors?</li>
        <li>Are solar poles worth the cost?</li>
        <li>Can we make use of IoT and wireless technologies to make our community more 
        sustainable?</li>
        <p style="text-align:justify">To investigate this, we looked into street 
        light data set from the City of Hobart, data on historical energy 
        usage and foot traffic in the CBD, as well as potentially intergrate street 
        into a Smart City.</p>
        """, unsafe_allow_html=True)

    LIGHT_FILE = 'light.csv'
    light = pd.read_csv(LIGHT_FILE)

    st.markdown("""<h2 style="text-align:center">Idea 1: Phasing out old MV lamps</h2>""",
                unsafe_allow_html=True)
    st.write("""
    <p style="text-align:justify">We wanted to evaluate each type of bulb for their 
    operational cost over 25,000 hours by standardising their wattage to 1700 lumens. 
    Assuming an electrical cost of $0.4/kWh, we can see the LED and HPS bulbs are 
    twice as efficient as MV and CFL bulbs. MV and CFL bulbs are the prime candida
    tes for replacement given their wattage to lumens inefficiency.</p>
    <p style="text-align:justify">Assuming the fixed cost of changing a bulb to a 
    different type is $700 and that we hope to recoup our expenses in 5 years, we 
    would need a wattage difference of 96 W to justify swapping to a more 
    efficient LED bulb.</p>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_cost(), use_container_width=True)

    st.header('Lighting Map')
    st.write(
        """ 
    <p style="text-align:justify">We visualised each street light in Hobart to 
    identify trends. We noticed that high wattage HPS and WV lights were used 
    on highways and major roads, with LED and CFL mainly used on minor roads 
    in residential areas.</p>
    <p style="text-align:justify">We recommend swapping out 400 W MV to 250 W 
    LED bulbs on major roads.</p>
    <p style="text-align:justify">We recommend swapping out 125 W and 150 W MV 
    to 18W LED bulbs on minor roads.</p>
    <p style="text-align:justify">Possible MV to LED swap outs have been 
    located in the map below.</p>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_lighting_map(light), use_container_width=True)

    st.markdown(
        'Below you can select which lamp type to view its distribution in Hobart:')
    lamp_type = st.selectbox('', [
                             'MV', 'CFL', 'LED', 'HPS'])
    lamp_type_desc_dict = {
        'MV': """
        <p style="text-align:justify">MV bulbs are the least efficient 
        and we recommend swapping them when applicable.</p>
        <p style="text-align:justify">We recommend swapping 400 W MV to 
        250 W LED bulbs on major roads. This is assuming that 250 W LED 
        lights have the equivalent luminosity to 250 W HPS lights. This 
        has the potential saving of $219 in electrical costs per annum, 
        and there are 155 possible replacements.</p>
        <p style="text-align:justify">We recommend swapping out 125W and 
        150 W MV to 18 W LED bulbs on minor roads.</p>

        """,

        'CFL': """
        <p style="text-align:justify">Due to the low wattage of CFL bulbs, 
        there are no gains from swapping them out into LEDs.</p>
        """,

        'LED': """
        <p style="text-align:justify">LED lights are our lights of choice 
        due to efficiency, life-span and ability to be dimmed. They are 
        the most used lights in smart cities and is the recommended light 
        for future-proofing. The light is directed to the ground with 
        minimal light pollution. For these reasons we recommend swapping 
        into LED lamps.</p>
        """,

        'HPS': """
        <p style="text-align:justify">The efficiency of HPS and LED lamps 
        are similar, there is no cost-benefit of swapping them to LEDs. 
        Dimming is not ideal for HPS bulbs as they take time to reach 
        maximum luminosity and it may reduce their life-span.</p>
        """
    }
    st.markdown(lamp_type_desc_dict[lamp_type], unsafe_allow_html=True)
    st.plotly_chart(plot_lamp_hist(light, lamp_type), use_container_width=True)

    st.markdown("""<h2 style="text-align:center">Idea 2: Metering, dimming and sensors</h2>""",
                unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:justify">For the council to see monetary benefit 
    from dimming with or without sensors, individual metering would need 
    to be installed on each light pole. We have focused our attention on 
    dimming in residential areas, as they are most likely the areas with 
    the most downtime at night. We have chosen not to consider dimming on 
    highways and major roads due to safety reasons.</p>
    <p style="text-align:justify">Dimming already efficient 18 W LED lights in 
    residential areas have minuscule gains of 3 hours saved per night. This is 
    an annual saving of $8 per meter installed per year. Given an expensive 
    upfront meter box installation cost, we cannot recommend dimming with or 
    without sensors on a purely financial level. However, dimming can reduce 
    greenhouse gas emissions, improve lightbulb lifespan and reduce light pollution.</p>

    """, unsafe_allow_html=True)

    st.markdown("""<h2 style="text-align:center">Idea 3: Adapting to solar</h2>""",
                unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:justify">Solar poles are powered by sun, a renewable
     energy source.</p>
    <p style="text-align:justify">We wanted to investigate and weigh up the 
    benefits and costs of installing solar poles as a permanent electrical 
    solution.</p>
    <p style="text-align:justify">Advantages:</p>
    <li>Solar poles take street lights off the grid permanently, which means 
    permanent electricity savings from usage per kilowatt hour as well as 
    network charges</li>
    <li>The lights are invulnerable to electricity outages, which provides 
    added safety to the city</li>
    <li>Solar poles have an average lifespan of 20 years and have low maintenance 
    costs associated with it</li>
    <li>Some solar poles also have a sensor option available, which can reduce 
    light pollution in areas that are deserted at night</li>
    <p style="text-align:justify">Disadvantages:</p>
    <li>High upfront cost</li>
    <li>Solar energy is dependant on weather factors such as UV index, cloud 
    coverage and daylight hours</li>

    <p style="text-align:justify">Our recommendation plan is a 4 phase solar 
    pole rollout for the City of Hobart. We looked at major foot traffic 
    areas to help determine which locations would provide the greatest 
    social benefit to help attract people towards the city centre. We 
    also made sure each phase was within the City of Hobart's annual 
    street light budget, making this a realistic plan. Using this information, 
    we created a visualization that shows the streets involved during each 
    phase and the annual savings from reduced energy and network costs.</p> 
    """, unsafe_allow_html=True)

    year_dict = {'Year 1': [1],
                 'Year 2': [2],
                 'Year 3': [3],
                 'Year 4': [4],
                 'All Years': [1, 2, 3, 4],
                 }
    st.markdown("""
    <p style="text-align:justify">In the drop down box you can select the 
    phases to see the spread of solar poles in the city, as well as the 
    annual savings per pole.</p>
    """, unsafe_allow_html=True)
    year_select = st.selectbox('', list(year_dict.keys()))
    solar_df = pd.read_csv('./solar_pole_table.csv')
    st.plotly_chart(plot_solar(solar_df, year_select),
                    use_container_width=True)
    solar_df = solar_df.drop(['Longitude', 'Latitude'], axis=1)[
        solar_df['Implementation year'].isin(year_dict[year_select])]
    solar_df = df_float_formatter(solar_df, formatter="{:.2f}")
    solar_df

    st.markdown("""<h2 style="text-align:center">Idea 4: Embracing a smart future</h2>""",
                unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align:justify">We know cities are constantly on the lookout 
    for smart solutions to enhance city vibrancy and promote local businesses 
    by attracting local and overseas tourists. With this in mind, we propose 
    building on the sustainable solar poles and adding in street friendly 
    features such as a solar charging station for small devices.<br>
    We also believe we can harness the power of IoT by connecting each 
    solar pole to a cloud. Councils are able to utilise these wireless 
    connections by feeding in inputs such as weather forecasts, UV 
    index, cloud coverage. This allows the council to adjust the dimming 
    to accommodate for special public events such as New Years, 
    which may draw large crowds out into the city late at night. 
    This flexibility provides the citizens with safe lighting, as 
    well as meeting the council's energy and sustainability requirements.</p>
    """, unsafe_allow_html=True)
    smart_city = Image.open(os.path.join('asset', 'smart_city.png'))
    st.image(smart_city, caption='How poles can be intergrated into Smart City',
             use_column_width=True)

    st.header('About')
    st.markdown("""
    <p style="text-align:justify">
    This web app is part of a submission for GovHack 2020 Hackathon, made by 
    <a href="https://www.linkedin.com/in/arnab-mukherjee-data/">Arnab Mukherjee</a>, 
    <a href="https://www.linkedin.com/in/emily-shen/">Emily Shen</a>, 
    <a href="https://www.linkedin.com/in/hengwang322/">Heng Wang</a>, and 
    <a href="https://www.linkedin.com/in/alfred-zou/">Alfred Zou</a>.
    <br>
    Feel free to check out our <a href="https://hackerspace.govhack.org/projects/lights_out">project page</a> 
    and <a href="https://github.com/hengwang322/lights_out">the repository</a>! 
    
    </p>""",
                unsafe_allow_html=True)


if __name__ == '__main__':
    main()
