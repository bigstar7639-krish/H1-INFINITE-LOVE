// Phase 12 - Weather
export type Weather = 'sunny'|'rainy'|'cloudy'|'snowy'|'stormy';
export interface WeatherConfig { particles: number; lightDim: number; sound: string; }
export const WEATHER_CONFIG: Record<Weather, WeatherConfig> = {
  sunny: { particles: 0, lightDim: 1.0, sound: 'birds' },
  rainy: { particles: 500, lightDim: 0.7, sound: 'rain' },
  cloudy: { particles: 0, lightDim: 0.8, sound: 'wind' },
  snowy: { particles: 400, lightDim: 0.85, sound: 'quiet' },
  stormy: { particles: 800, lightDim: 0.5, sound: 'thunder' },
};
