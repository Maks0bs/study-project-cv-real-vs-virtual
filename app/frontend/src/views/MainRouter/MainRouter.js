import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import MainMenu from './components/MainMenu';
import Main from './views/Main';
import RunDetection from './views/RunDetection';
import DetectionDetail from './views/DetectionDetail';
import {join as joinPaths} from 'path';

/**
 * @namespace components.views.classroom
 */

/**
 * This router is responsible for routing to all links that are
 * used by authenticated users. This is the core of the website,
 * all most important features are on this router
 * @memberOf components.views.classroom
 * @component
 */
class MainRouter extends Component {

	render() {
		let { path } = this.props.match;
		return (
			<div>
				<MainMenu {...this.props} />
				<Switch>
					<Route
						exact path={`${path}`}
						component={Main}
					/>
					<Route
						exact path={`${joinPaths(path, 'run')}`}
						component={RunDetection}
					/>
					<Route
						exact path={`${joinPaths(path, 'overview')}`}
						component={RunDetection}
					/>
					<Route
						exact path={`${joinPaths(path, 'detection', ':id')}`}
						component={DetectionDetail}
					/>
				</Switch>
			</div>
		);
	}
}

export default MainRouter;