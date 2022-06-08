import {Component} from 'react';
import PropTypes from 'prop-types';

import MUITabPanel from '@mui/lab/TabPanel';


class TabPanel extends Component {
    render = () => {
        return (
            <MUITabPanel
                value={this.props.value}
                sx={{padding: 0}}
            >
                {this.props.children}
            </MUITabPanel>
        )
    }
}


TabPanel.propTypes = {
    value: PropTypes.string.isRequired
}

export default TabPanel;