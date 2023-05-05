import type { V2_MetaFunction } from '@remix-run/cloudflare';
import { useLoaderData } from '@remix-run/react';
import { parseISO, format } from 'date-fns';

import { useState, memo, useMemo } from 'react';
import { PlusIcon } from '@heroicons/react/20/solid';
import MobileFilter from '~/Components/MobileFilter';

import ClassListItem from '~/Components/YogaClass';
import { DayClasses } from '~/types';
import { createFiltersFromClasses, useFilterReducer } from '~/filterReducer';

const MemoizedClassListItem = memo(ClassListItem);

export const loader = async (): Promise<DayClasses> => {
  const data = (await CLASSES.get('data', { type: 'json' })) as DayClasses;

  return data;
};

export const meta: V2_MetaFunction = () => {
  return [{ title: 'yoga.prague' }];
};

export default function Example() {
  const days = useLoaderData<typeof loader>();
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);
  const { handleCheck, state } = useFilterReducer();

  const filters = useMemo(() => createFiltersFromClasses(days), [days]);

  const filteredDays = useMemo(() => {
    return days
      .map((day) => ({
        date: day.date,
        items: day.items.filter(
          (item) =>
            !state.location.length || state.location.includes(item.location),
        ),
      }))
      .filter((day) => day.items.length);
  }, [days, state]);

  return (
    <div className="bg-white">
      <MobileFilter
        {...{ filters, mobileFiltersOpen, setMobileFiltersOpen, handleCheck }}
      />
      <div>
        <main className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
          <div className="border-b border-gray-200 pb-10">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900"></h1>
            <p className="mt-4 text-base text-gray-500"></p>
          </div>

          <div className="pt-12 lg:grid lg:grid-cols-3 lg:gap-x-8 xl:grid-cols-4">
            <aside>
              <h2 className="sr-only">Filters</h2>

              <button
                type="button"
                className="inline-flex items-center lg:hidden"
                onClick={() => setMobileFiltersOpen(true)}
              >
                <span className="text-sm font-medium text-gray-700">
                  Filters
                </span>
                <PlusIcon
                  className="ml-1 h-5 w-5 flex-shrink-0 text-gray-400"
                  aria-hidden="true"
                />
              </button>

              <div className="hidden lg:block">
                <form className="space-y-10 divide-y divide-gray-200">
                  {filters.map((section, sectionIdx) => (
                    <div
                      key={section.name}
                      className={sectionIdx === 0 ? '' : 'pt-10'}
                    >
                      <fieldset>
                        <legend className="block text-sm font-medium text-gray-900">
                          {section.name}
                        </legend>
                        <div className="space-y-3 pt-6">
                          {section.options.map((option, optionIdx) => (
                            <div key={option} className="flex items-center">
                              <input
                                id={`${section.id}-${optionIdx}`}
                                name={section.id}
                                value={option}
                                onChange={handleCheck}
                                type="checkbox"
                                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                              />
                              <label
                                htmlFor={`${section.id}-${optionIdx}`}
                                className="ml-3 text-sm text-gray-600"
                              >
                                {option}
                              </label>
                            </div>
                          ))}
                        </div>
                      </fieldset>
                    </div>
                  ))}
                </form>
              </div>
            </aside>

            <div className="mt-6 lg:col-span-2 lg:mt-0 xl:col-span-3">
              {filteredDays.map((day) => (
                <div key={day.date}>
                  <h3 className="truncate text-base font-medium leading-7 text-slate-900">
                    {format(parseISO(day.date), 'PPPP')}
                  </h3>
                  <ol className="mt-4 divide-y divide-gray-100 text-sm leading-6 lg:col-span-7 xl:col-span-8">
                    {day.items.map((activity) => (
                      <MemoizedClassListItem
                        key={activity.activity_id}
                        lesson={activity}
                      />
                    ))}
                  </ol>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
