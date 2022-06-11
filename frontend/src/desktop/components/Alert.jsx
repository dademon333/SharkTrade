import {Component} from 'react';
import {Snackbar, Alert as MUIAlert} from '@mui/material';
import PropTypes from 'prop-types';

import {alertChanged} from '../../slices/Global';
import {connect} from 'react-redux';
import AlertSeverity from '../../constants/AlertSeverity';


class Alert extends Component {
    getStyles = (severity) => {
        let color;
        switch (severity) {
            case AlertSeverity.SUCCESS:
                color = 'var(--primary-green)';
                break;
            case AlertSeverity.INFO:
                color = 'var(--primary-blue)';
                break;
            case AlertSeverity.WARNING:
                color = 'var(--primary-orange)';
                break;
            case AlertSeverity.ERROR:
                color = 'var(--primary-red)';
                break;
            default:
                color = 'var(--primary-green)';
        }

        return {
            border: `2px solid ${color}`,
            borderRadius: '8px',
            fontSize: 16,
            fontWeight: 500,

            '& .MuiAlert-icon, & .MuiAlert-message, & .MuiAlert-action': {
                color: color
            },
        }
    }

    render = () => {
        const {severity, variant, children} = this.props;
        const sx = this.getStyles(severity);

        return (
            <Snackbar
                open={true}
                autoHideDuration={10000}
                onClose={() => this.props.alertChanged(null)}
            >
                <MUIAlert
                    sx={sx}
                    severity={severity}
                    variant={variant}
                    onClose={() => this.props.alertChanged(null)}
                >
                    {children}
                </MUIAlert>
            </Snackbar>
        )
    }
}


Alert.propTypes = {
    severity: PropTypes.string.isRequired,
    variant: PropTypes.string.isRequired
}

const mapDispatchToProps = {
    alertChanged
}

export default connect(null, mapDispatchToProps)(Alert);