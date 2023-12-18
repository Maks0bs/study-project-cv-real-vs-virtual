import React, { Component } from 'react';

/**
 * Lists all courses that are relevant to the user
 * and also the list of all open courses
 * @memberOf components.views.classroom
 * @component
 */
class CourseList extends Component {

	displayError = (text) => {
		return this.props.addToast(
			(<div>{text.message || text || 'Error occurred'}</div>),
			{type: 'error'}
		)
	}
	// Receives course lists, handles errors and adds notifications
	handleCourseListData = (payload) => {
		if (this.props.error) {
			return this.displayError(this.props.error.message || this.props.error);
		}
		return this.props.addNotViewedNotifications(
			// Extract IDs from the whole course data
			Array.isArray(payload) ? payload.map(c => c._id) : []
		)
			.then(() => {
				if (this.props.error) throw {
					message: 'Problem with loading courses'
				}
			})
			.catch(err => this.displayError(err.message))
	}

	shouldComponentUpdate(nextProps, nextState, nextContext) {
		if (!this.props.authenticatedUser && nextProps.authenticatedUser) {
			this.initData(nextProps.authenticatedUser);
		}
		return true;
	}

	initData = (user) => {
		this.props.setLoading('open' , true);
		this.props.getOpenCourses()

		let isAuthenticated = user && user._id;
		if (isAuthenticated) {
			this.props.setLoading('enrolled' , true);
			this.props.getEnrolledCourses(user._id)
				.then(() => this.handleCourseListData(this.props.enrolledCourses))
			if (user.role === 'teacher') {
				this.props.setLoading('teacher', true);
				this.props.getTeacherCourses(user._id)
					.then(() => this.handleCourseListData(this.props.teacherCourses));
			}

		}
	}

	componentDidMount() {
		this.initData(this.props.authenticatedUser);
	}

	componentWillUnmount() {this.props.cleanup()}

	render() {
		let { authenticatedUser: user } = this.props;
		let isAuthenticated = user && user._id;

		return (
			<div className="container my-5">
				dsds
			</div>
		);
	}
}


export default CourseList