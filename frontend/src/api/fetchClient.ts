type QueryParams = Record<string, number | string | undefined>;

type FetchClientOptions = {
  query?: QueryParams;
};

export class FetchError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = 'FetchError';
    this.status = status;
  }
}

const getBackendUrl = () => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  if (!backendUrl) {
    throw new Error('Не задан адрес сервера');
  }

  return backendUrl.replace(/\/$/, '');
};

const buildQueryString = (query?: QueryParams) => {
  const params = new URLSearchParams();

  Object.entries(query ?? {}).forEach(([key, value]) => {
    const trimmedValue = value?.toString().trim();

    if (trimmedValue) {
      params.set(key, trimmedValue);
    }
  });

  return params.toString();
};

export const get = async <ResponseBody>(
  path: string,
  options: FetchClientOptions = {},
): Promise<ResponseBody> => {
  const queryString = buildQueryString(options.query);
  const url = `${getBackendUrl()}${path}${queryString ? `?${queryString}` : ''}`;

  let response: Response;

  try {
    response = await fetch(url);
  } catch {
    throw new Error('Не удалось подключиться к серверу.');
  }

  if (!response.ok) {
    throw new FetchError(response.status, 'Ошибка сервера при загрузке данных.');
  }

  try {
    return (await response.json()) as ResponseBody;
  } catch {
    throw new Error('Сервер вернул некорректный ответ');
  }
};
