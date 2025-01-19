import React, { Component } from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { AnimatePresence, motion } from 'framer-motion';
import { BrowserRouter, Route, Switch, useLocation } from 'react-router-dom';
import './App.css';

import Home from './components/home/App';




class App extends Component {
	render() {
		return (
			<div class="App">


				<Navbar fixed="top" bg="dark" variant="dark">
					<Navbar.Brand href="/">Home</Navbar.Brand>
					<Nav className="mr-auto">
						<Nav.Link href="/visu">Visualise</Nav.Link>
						<Nav.Link href="/bolly">Bollywood</Nav.Link>
					</Nav>
					<Nav>
						<Nav.Link href="/team">Team</Nav.Link>
						<Nav.Link eventKey={2} href="/contact">
							Contact Us
						</Nav.Link>
					</Nav>

				</Navbar>
				<AnimatePresence >
					<Switch>
						<Route path="/" component={Home} exact />
					
					</Switch>
				</AnimatePresence>
			</div>
		);
	}
}

export default App;
