import React, { Component } from 'react';

/**
 * Used to display modals with any custom component inside
 * There should only be one ModalRoot per app
 *
 * @memberOf components.views.serviceComponents
 * @component
 */
class Settings extends Component {
    constructor(props){
        super(props);
        const settings = JSON.parse(localStorage.getItem('detection_settings'));
        this.state = {scoreThreshold: settings?.scoreThreshold, boxesCount: settings?.boxesCount}
    }

    handleChange = (name) => (e) => {
        this.setState({
            [name]: e.target.value
        })
    }

    handleLeave = () => {
        this.props.hideModal();
    }

    componentWillUnmount() {
        this.handleLeave();
    }

    onSubmit = (e) => {
        e.preventDefault();
        localStorage.setItem('detection_settings', JSON.stringify({...this.state}))
        this.handleLeave()
    }


    render() {
        let {scoreThreshold, boxesCount} = this.state;
        let isMobileWidth = (window.innerWidth <= 1000)
        return (
            <div>
                <div
                    className="container text-center my-3"
                    style={{width: isMobileWidth ? '90%' : '60%'}}
                >
                    <form>
                        <div className="form-group">
                            <label className="text-muted">Score threshold to count as a detection</label>
                            <input
                                onChange={this.handleChange("scoreThreshold")}
                                type="number"
                                step="0.001"
                                className="form-control"
                                value={scoreThreshold}
                            />
                        </div>
                        <div className="form-group">
                            <label className="text-muted">Max amount of boxes to detect</label>
                            <input 
                                onChange={this.handleChange("boxesCount")}
                                type="number" 
                                step="1"
                                className="form-control"
                                value={boxesCount}
                            />
                        </div>
                        <button 
                            className="btn btn-outline btn-raised"
                            onClick={this.onSubmit}
                        >
                            Save
                        </button>
                    </form>
                </div>
            </div>
        )
    }
}

export default Settings