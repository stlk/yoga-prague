export type YogaClass = {
  activity_name: string;
  activity_id: number;
  time_start: string;
  time_end: string;
  instructor_name: string;
  instructor_photo: null | string;
  price: string;
  free_spaces: number;
  has_free_spaces: boolean;
  link: string;
  location: string;
  time_start_human: string;
  time_end_human: string;
  finished: boolean;
};

export type DayClasses = {
  date: string;
  items: YogaClass[];
}[];
