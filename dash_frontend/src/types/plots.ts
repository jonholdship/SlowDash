export interface DataPoint{
	x: any;
	y: number;
}

export interface Plots {
	pace_plot: DataPoint[];
	hr_plot: DataPoint[];
  }