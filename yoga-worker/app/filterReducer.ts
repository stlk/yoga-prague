import { useReducer } from 'react';
import { DayClasses } from './types';

type State = {
  [key: string]: string[];
};

type Action = {
  type: 'handle_check';
  field: string;
  value: string;
};

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'handle_check':
      let filter = state[action.field] || [];
      filter = filter.includes(action.value)
        ? filter.filter((location) => location !== action.value)
        : [...filter, action.value];
      return { ...state, [action.field]: filter };
    default:
      return state;
  }
};

const initialState: State = {
  location: [],
};

export function useFilterReducer() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return {
    state,
    handleCheck(event: React.ChangeEvent<HTMLInputElement>) {
      dispatch({
        type: 'handle_check',
        field: event.target.name,
        value: event.target.value,
      });
    },
  };
}

type FilterOption = {
  id: string;
  name: string;
  options: string[];
};

export const createFiltersFromClasses = (
  dayClasses: DayClasses,
): FilterOption[] => {
  const activities: Set<string> = new Set();
  const instructors: Set<string> = new Set();
  const locations: Set<string> = new Set();

  dayClasses.forEach((dayClass) => {
    dayClass.items.forEach((yogaClass) => {
      // activities.add(yogaClass.activity_name);
      // instructors.add(yogaClass.instructor_name);
      locations.add(yogaClass.location);
    });
  });

  const filters: FilterOption[] = [
    // {
    //     id: 'activity_name',
    //     name: 'Activity Name',
    //     options: Array.from(activities),
    // },
    // {
    //     id: 'instructor_name',
    //     name: 'Instructor Name',
    //     options: Array.from(instructors),
    // },
    {
      id: 'location',
      name: 'Location',
      options: Array.from(locations),
    },
  ];

  return filters;
};
