import os

import streamlit as st
import pandas as pd
import plotly.express as px

from src.plot import plot_cost, plot_lighting_map, plot_lamp_hist

MAPBOX_TOKEN = os.environ['MAPBOX_TOKEN']


def main():
    st.beta_set_page_config(page_title='Lights Out!',
                            page_icon="💡",
                            layout='wide')
    st.markdown("""<h1 style="text-align:center">Lights Out!</h1>""",
                unsafe_allow_html=True)

    LIGHT_FILE = 'light.csv'
    light = pd.read_csv(LIGHT_FILE)

    st.header('Operational Costs')
    st.write("""
    * To calculate the operational cost, we first standardise each type of light 
    to 1700 lumens (a suitable light level for residential lighting)
    * We calculate the operational cost over a 25,000 hour life span, which 
    includes electrical cost at $0.4/kwh and the cost of each light. This 
    standardises all the lights based on life span as well
    * We can see that LED and HPS lights are the best performers with 
    approximately half the cost of MV and CFL lights""")
    st.plotly_chart(plot_cost(), use_container_width=True)

    st.header('Lighting Map')
    st.write(
        """ 
    * Each type of light is plotted onto a map of Hobart
        * We can see two major trends:
        * HPS and MV lights are used for lighting up major roads
    * Where as LED AND CFL lights are mainly for minor roads and 
    residential areas
    * Possible MV replacements have been marked as POI (points of interest)
        * POI (20W LED) means potential to replace with 20W LED (Square)
        * POI (250W LED) means potential to replace with 250W LED (Circle)""")
    st.plotly_chart(plot_lighting_map(light), use_container_width=True)

    st.header('Light Replacement')
    st.write(
        """
    * Assuming the fixed cost of changing to a different type of light is \$700 
    * Assuming we hope to recover our light replacement cost in 5 years
    * We would need approximately an energy saving of $140/yr
    * Assuming each kwh is $0.40 saved, we would need save 350kwh/yr
    * This equates to a wattage difference of 96 to justify swapping out a less 
    efficient light for a LED light
    """
    )

    st.header('Metering installation & Sensors')
    st.write(
        """
    * Assume we want to implement some sort of dimming strategy. The council 
    will only gain monetary benefit if there is metering installed
    * Assuming the fixed cost of installing metering is \$500 to include the 
    cost of parts, electrician and a cherry picker 
    * Assuming we hope to recover our light replacement cost in 5 years
    * We would need approximately an energy saving of $100/yr
    * Dimming can only be applied to LED lights
    * In the context of 18W LED lights and a dimming profile would save 3hrs 
    per night, we save approximately \$8 per light/yr.
    * Installing metering for each light pole cannot be justified.
    * Similarly for the idea of installing sensors.
    * Reducing wattage is by far the most effective and recommended strategy""")

    lamp_type = st.selectbox('Select a light type', [
                             'MV', 'CFL', 'LED', 'HPS'])
    lamp_type_desc_dict = {
        'MV': """
        * By plotting the distribution of MV lights, we can see that MV lights 
        can be clustered into two categories:
        * less than or equal to 150, and
            * more than 150 for major road lighting
            * For the first case we could replace 125 and 150W bulbs with 18W 
            LED lights in residential areas.
        * For the second case we could replace 400W bulbs with 250W LED light 
        on major roads. This is assuming that 250W LED 
        lights have the equivalent luminosity to 250W HPS lights. This has the 
        potential saving of $219 in electrical 
        costs per annum, and there are 155 possible replacements""",

        'CFL': """
        * Due to the low wattage, there doesn't seem to be any benefit of 
        monetary benefit of swapping to LED light.""",

        'LED': """
        * Most of the LED lights are in residential areas
        * LED lights provide the benefit of dimming, so they have the greatest 
        benefit in residential areas
        * They have similar luminosity to HPS lights, so there is no justifiable 
        reason to replace HPS lights with LED lights
        * We assume no dimming is used on major roads for safety
        * LED lights do have the benefit of integrating into a smart network and 
        is the recommended path towards a smart city""",

        'HPS': """
        * HPS lights have similar luminosity to LED lights, so there is no 
        justifiable reason to replace them with LED lights
        """
    }
    st.write(lamp_type_desc_dict[lamp_type])
    st.plotly_chart(plot_lamp_hist(light, lamp_type), use_container_width=True)


if __name__ == '__main__':
    main()
