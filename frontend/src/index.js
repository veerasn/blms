import React from "react";
import ReactDOM from "react-dom";

import App from "./components/App";

const el = <h1>That's some progress!</h1>
ReactDOM.render(el, document.getElementById('root'));

class Car {
    constructor(name, cc) {
        this.brand = name
        this.capacity = cc
    }

    present(){
        return 'I have a ' + this.brand + ' which is ' + this.capacity;
    }
}

mycar = new Car('BMW', 1200);
mycar.present();