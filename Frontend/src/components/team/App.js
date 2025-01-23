import React, { Component } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import './App.css';
import { Switch } from 'react-router-dom';
const pageVariants = {
	initial: {
		opacity: 0,
		x: "-100%",
		scale: 0.8
	},
	in: {
		opacity: 1,
		x: 0,
		scale: 1
	},
	out: {
		opacity: 0,
		x: "100%",
		scale: 1.2
	}
};
const pageTransition = {
	type: "tween",
	ease: "anticipate",
	duration: 0.5
};
class App extends Component {




	render() {



		return (
			<main>
				<Switch>
					<motion.div className="App" initial="initial" exit="out" animate="in" variants={pageVariants} transition={pageTransition} >

						<div class="container">
							<div class="section-title">
								<h1>Meet the Team</h1>
							</div>
							<div class="row">
								<div class="column">
									<div class="team-4">
										<div class="team-content">
											<h2>Ayush Kumar</h2>
											<h3>iec2022004@iiita.ac.in</h3>
										</div>
										<div class="team-img">
											<img src={require("./img/ayushimg.jpeg")} alt="Team Image" />
											<div class="team-content">
												<p>Primarily worked on building React based Frontend and Neo4j-Django integration</p>
											</div>
										</div>
										<div class="team-content">
											<div class="team-social">

												
												<a class="social-li" href="https://www.linkedin.com/in/ayush-kumar-743122256//" target="_blank" rel="noopener noreferrer"><i class="fab fa-linkedin-in"></i></a>
												<a class="social-in" href="https://www.instagram.com/7_puffsonly/" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
												<a class="social-gi" href="https://github.com/Guanidine4336" target="_blank" rel="noopener noreferrer"><i class="fab fa-github"></i></a>

											</div>
										</div>
									</div>
								</div>
								
								<div class="column">
									<div class="team-4">
										<div class="team-content">
											<h2>Srijan Jain</h2>
											<h3>iit2022156@iiita.ac.in</h3>
										</div>
										<div class="team-img">
											<img src={require("./img/srijan.jpeg")} alt="Team Image" />
											<div class="team-content">
												<p>Optimised the scraping and worked on Django backend development</p>
											</div>
										</div>
										<div class="team-content">
											<div class="team-social">

												
												<a class="social-li" href="https://www.linkedin.com/in/fremder/" target="_blank" rel="noopener noreferrer"><i class="fab fa-linkedin-in"></i></a>
												<a class="social-in" href="https://www.instagram.com/fremdder/" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
												<a class="social-gi" href="https://github.com/fremdder" target="_blank" rel="noopener noreferrer"><i class="fab fa-github"></i></a>
											</div>
										</div>
									</div>
								</div>

							</div>
						</div>
					</motion.div>
				</Switch>
			</main >
		);
	}
}

export default App;
