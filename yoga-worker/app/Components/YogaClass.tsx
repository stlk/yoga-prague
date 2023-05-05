import { CalendarIcon, MapPinIcon } from '@heroicons/react/20/solid';
import { format, parseISO, isPast } from 'date-fns';
import { YogaClass } from '~/types';

function extractInitials(name: string) {
  let initials = '';

  // split the name into an array of words
  const words = name.split(' ');

  // loop through each word in the array
  for (let i = 0; i < words.length; i++) {
    if (words[i].length > 2) {
      // get the first letter of each word and add it to the initials string
      initials += words[i].charAt(0);
    }
  }

  // return the initials in uppercase
  return initials.toUpperCase();
}

export default function ClassListItem({ lesson }: { lesson: YogaClass }) {
  const time_start = parseISO(lesson.time_start);
  const time_end = parseISO(lesson.time_end);
  const lessonEnded = isPast(time_end);

  return (
    <li
      key={lesson.activity_id}
      className="relative flex space-x-6 py-6 xl:static"
    >
      {lesson.instructor_photo ? (
        <img
          src={lesson.instructor_photo}
          alt=""
          className="h-14 w-14 flex-none rounded-full"
        />
      ) : (
        <span className="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
          <span className="text-xl font-medium leading-none text-white">
            {extractInitials(lesson.instructor_name)}
          </span>
        </span>
      )}

      <div className="flex-auto">
        <h3 className={`pr-10 font-semibold text-gray-900 xl:pr-0`}>
          {lesson.activity_name}
        </h3>
        <p className="pr-10 text-gray-500 xl:pr-0">{lesson.instructor_name}</p>
        <dl className="mt-2 flex flex-col text-gray-500 xl:flex-row">
          <div className="flex items-start space-x-3">
            <dt className="mt-0.5">
              <span className="sr-only">Date</span>
              <CalendarIcon
                className="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
            </dt>
            <dd className={`${lessonEnded && 'line-through'}`}>
              <time dateTime={lesson.time_start}>
                {format(time_start, 'p')} - {format(time_end, 'p')}
              </time>
            </dd>
          </div>
          <div className="mt-2 flex items-start space-x-3 xl:ml-3.5 xl:mt-0 xl:border-l xl:border-gray-400 xl:border-opacity-50 xl:pl-3.5">
            <dt className="mt-0.5">
              <span className="sr-only">Location</span>
              <MapPinIcon
                className="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
            </dt>
            <dd>{lesson.location}</dd>
          </div>
        </dl>
      </div>
    </li>
  );
}
