import React from 'react';
import { useState, useEffect } from 'react';
import QueryForm from './components/QueryForm';
import ResultsGrid from './components/ResultsGrid';

function App() {
	const [itemGrid, setItemGrid] = useState(null);
	const [count, setCount] = useState(0);
	const [currentTime, setCurrentTime] = useState(0);
	
	const backendURL = import.meta.env.VITE_BACKEND_URL; // https://vite.dev/guide/env-and-mode.html

	
	function performSampleQuery() {
		console.log("Asking API for data...");

		// 1. Reach out to API.
		// 2. Get API to send you the results of a query.
		// 3. Pass the query results to the item grid.		

		//setItemGrid(results);
	}

	function checkReadyAPI() {
		console.log("Sending query...");	
		console.log(backendURL + '/api/ready');
		fetch
		(
			backendURL + '/api/ready'
		).then(
			response => {
				if (response.ok) {
					return response.json();
				}
				throw response; // will be handled by catch
			}
		).then(
			data => {
				console.log("Query results received!");
				console.log(data);
			}
		).catch(
			exception => {
				console.log("Couldn't connect!");
				throw exception;
			}
		);
	}



	return (
		<>
			<p>if you see this then congrats, it's working</p>
			<div className="upper">
				<button onClick={() => setCount((count) => count + 1)}>
					count is {count}
				</button>
				<button onClick={checkReadyAPI}>
					Sample Query
				</button>
				<p>
					Edit <code>src/App.jsx</code> and save to test HMR.
				</p>
				<QueryForm
					runQuery={performSampleQuery}
					defaultQueryText={"put a query here"}
				/>			
			</div>
			<div className="lower">
				<ResultsGrid
					itemGrid={itemGrid}
				/>
			</div>
		</>
	);
}

export default App;