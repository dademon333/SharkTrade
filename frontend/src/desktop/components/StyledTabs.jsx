import {Component} from 'react';
import {Tabs} from '@mui/material';
import PropTypes from 'prop-types';


class StyledTabs extends Component {
    render = () => {
        const {value, children, onChange} = this.props;
        return (
            <Tabs
                value={value}
                onChange={onChange}
                sx={{
                    minHeight: 40,
                    maxHeight: 40,
                    '& button': {
                        textTransform: 'none',
                    },
                    '& .MuiButtonBase-root': {
                        color: 'var(--bright-quaternary)',
                        fontSize: 18,
                        lineHeight: '16px',
                        fontWeight: 400,
                        minHeight: 40,
                        maxHeight: 40,
                        minWidth: 150,
                        boxShadow: 'inset 0 0 0 0',
                    },
                    '& .MuiButtonBase-root.Mui-selected': {
                        color: 'var(--bright-primary)',
                        fontWeight: 500,
                        boxShadow: 'inset 0px -16px 8px -10px rgba(199, 203, 209, 0.2)'
                    },
                    '& .MuiTabs-indicator': {
                        backgroundColor: 'var(--primary-green)'
                    },
                }}
            >
                {children}
            </Tabs>
        )
    }
}


StyledTabs.propTypes = {
    value: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired
}

export default StyledTabs;