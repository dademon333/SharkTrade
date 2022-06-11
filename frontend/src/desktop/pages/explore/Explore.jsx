import {Component} from 'react';
import {Tab} from '@mui/material';
import TabContext from '@mui/lab/TabContext';

import StyledTabs from '../../components/StyledTabs';
import Template from '../../template/Template';
import AllLots from './AllLots';
import OwnLots from './OwnLots';
import Bids from './Bids';
import TabPanel from '../../components/TabPanel';

import './scss/Explore.scss';


class Explore extends Component {
    state = {
        activeTab: '1'
    }

    onActiveTabChange = (event, newValue) => {
        this.setState({activeTab: newValue});
    }

    render = () => {
        return (
            <Template navigation={true} className="explore">
                <TabContext value={this.state.activeTab}>
                    <StyledTabs value={this.state.activeTab} onChange={this.onActiveTabChange}>
                        <Tab value="1" label="Все лоты"/>
                        <Tab value="2" label="Мои лоты"/>
                        <Tab value="3" label="Мои ставки"/>
                    </StyledTabs>
                    <TabPanel value="1"> <AllLots /> </TabPanel>
                    <TabPanel value="2"> <OwnLots /> </TabPanel>
                    <TabPanel value="3"> <Bids /> </TabPanel>
                </TabContext>
            </Template>
        )
    }
}



export default Explore;