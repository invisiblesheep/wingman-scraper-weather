import Koa from 'koa';
import KoaRouter from 'koa-router';
import parse from 'co-body';
import serve from 'koa-static';
import mongoose from 'mongoose';
import cron from 'node-cron';
import { exec } from 'child_process';
const request = require('request');

import config from './config';

const app = new Koa();
const router = new KoaRouter({ prefix: '/api' });

let url = "http://localhost:1337/api";

let timeZone = 'Europe/Helsinki';

// exec(`python WeatherReportGenerator.py`, (err, stdout, stderr) => {
//     if (err) {
//         console.log(err, 'errors');
//         return;
//     }
//
//     // console.log(`stdout: ${stdout}`);
//     // console.log(`stderr: ${stderr}`);
//     // console.log(`stdout: ${stdout}`);
//     if (stdout) {
//         runModelOnWeatherReport(stdout);
//     }
// });

let CronJob = require('cron').CronJob;
new CronJob('* * * * *', function() {
    console.log('Getting weather report');
    exec(`python WeatherReportGenerator.py`, (err, stdout, stderr) => {
        if (err) {
            console.log(err, 'errors');
            return;
        }

        if (stdout) {
            runModelOnWeatherReport(stdout);
        }
    });

}, null, true, timeZone);

app.use(serve(`${__dirname}/../app/build/`));

app
    .use(router.routes())
    .use(router.allowedMethods());

function startKoa() {
    app.listen(config.koa.port);
    console.log(`Listening on port ${config.koa.port}`);
}

function runModelOnWeatherReport(input){

    exec(`python PredictInputWeather.py "${input}"`, (err, stdout, stderr) => {
        if (err) {
            console.log(err, 'errors');
            return;
        }

        console.log(`stdout: ${stdout[2]}`);
        console.log(`stderr: ${stderr}`);

        var story = "";
        if (stdout[2] === '0') {
            story = "Weather normal at HEL"
        } else if(stdout[2] === '1') {
            story = "Weather caution at HEL"
        } else {
            story = "Weather warning at HEL"
        }

        let today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();

        let wing = {};
        wing.heading = `Weather report ${mm +'/'+ dd +'/'+ yyyy}`;
        wing.story = story;
        wing.url = 'weatherscraper';
        wing.categories = 'weather';
        wing.impact = stdout[2];
        wing.source = 'weather-scraper';

        request({
            url: `${url}/wing`,
            method: "POST",
            json: wing
        })

    });

}

startKoa();