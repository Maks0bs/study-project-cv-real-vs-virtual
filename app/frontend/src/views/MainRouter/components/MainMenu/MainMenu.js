import React, { Component } from 'react';
import { Redirect } from 'react-router-dom'
import Settings from '../../../components/Settings'
import { FontAwesomeIcon as Icon } from '@fortawesome/react-fontawesome'
import { faCog } from '@fortawesome/free-solid-svg-icons'
import NavItem from "../../../../components/reusables/navbar/NavItem";
import ModalRoot from '../../../../components/ModalRoot/ModalRoot';

/**
 * This navigation bar is displayed on all pages, that
 * are indexed by the {@link components.views.classroom.ClassroomRouter}
 * @memberOf components.views.classroom
 * @component
 */
class ClassroomMenu extends Component {
	constructor(props){
		super(props);
		this.state = {
			display: false,
			settingsIconInFocus: false,
			showSettings: false,
		}
	}

	toggleSettingsHover = (e) => {
		e.preventDefault();
		this.setState({settingsIconInFocus: !this.state.settingsIconInFocus});
	}

	showSettingsModal = () => {
		this.setState({showSettings: true});
	}

	hideSettingsModal = () => {
		this.setState({showSettings: false});
	}

	toggleNavbar = (e) => {
		e.preventDefault();
		this.setState({display: !this.state.display});
	}
			
	render() {
		let { pathname } = this.props.location;
		let { redirectToHome, display, showSettings } = this.state;
		return (
			<nav className="navbar navbar-expand-lg navbar-light bg-light sticky-top">
				<ModalRoot show={showSettings} hideModal={this.hideSettingsModal}>
					{showSettings && (
						<Settings hideModal={this.hideSettingsModal}/>
					)}
				</ModalRoot>
				<button
					className="navbar-toggler"
					type="button"
					onClick={this.toggleNavbar}
				>
					<span className="navbar-toggler-icon" />
				</button>
				<div className={(display ? '' : 'collapse ') + "navbar-collapse"}>
					<NavItem pageURI={pathname} path={pathname} name="Animal detector" brand/>
					<ul className="navbar-nav mr-auto">
						<NavItem
							pageURI={pathname}
							path="/run"
							name="Run detection"
							key={-2}
						/>
						<NavItem
							pageURI={pathname}
							path="/overview"
							name="History"
							key={-1}
						/>
					</ul>
					<ul className="navbar-nav">
						<Icon
							className='link-primary'
							type='button'
							style={{display: 'flex', cursor: 'pointer', color: this.state?.settingsIconInFocus ? 'black' : 'gray'}}
							icon={faCog}
							size={'2x'}
							onClick={this.showSettingsModal}
							onMouseEnter={this.toggleSettingsHover} 
							onMouseLeave={this.toggleSettingsHover}
						/>
					</ul>
					{redirectToHome && (<Redirect to="/" />)}
				</div>
			</nav>
		);
	}
}

export default ClassroomMenu