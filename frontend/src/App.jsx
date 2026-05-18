import React from 'react';
import { useState, useEffect } from 'react';
import QueryForm from './components/QueryForm';
import ResultsGrid from './components/ResultsGrid';
import './App.css';

function App() {
	const [statusMessage, setStatusMessage] =  useState("Awaiting query...");
	const [statusError, setStatusError] =  useState(false);
	const [itemGrid, setItemGrid] = useState(null);
	const [count, setCount] = useState(0);
	const [currentTime, setCurrentTime] = useState(0);
	//const backendURL = import.meta.env.VITE_BACKEND_URL; // https://vite.dev/guide/env-and-mode.html

	const defaultQuery = `
	SELECT *
	FROM information_schema.tables
	WHERE table_schema= 'public'
	ORDER BY table_name;`;
	

	// NOTE: React knows where to send fetch requests, see vite.config.js	


	function runQuery(query) {
		console.log("Sending query...");	
		fetch(
			'/api/query?' + new URLSearchParams( {query: query} )
		).then(
			response => {
				console.log("Response received, status code: " + response.status);
				console.log(response);
				setStatusError(!response.ok);
				if (response.status === 400){
					console.log("Here dat boi");
					console.log(response.json());
				}
				if (response.ok) {
					setStatusMessage("Query executed successfully.");
					if (response.status === 204){
						return Promise.resolve(null);
					}else{
						let data = response.json();
						console.log(data);
						return data;
					}
				}
				setStatusMessage("Something bad happened. (add better error-handling later)");
				throw response; // will be handled by catch
			}
		).then(
			data => {
				console.log("Query results received!");
				if (data != null){
					setItemGrid(data);
				}
				console.log(data);
			}
		).catch(
			exception => {
				// put any specific error-handling here
				console.log("...and then an error occurred.");
				//throw exception; // enable anytime you want to see the details in the log
			}
		);
	}



	return (
		<>
			<div className="upper">
				<QueryForm
					runQuery={runQuery}
					defaultQueryText={defaultQuery}
					statusMessage={statusMessage}
					statusError={statusError}
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