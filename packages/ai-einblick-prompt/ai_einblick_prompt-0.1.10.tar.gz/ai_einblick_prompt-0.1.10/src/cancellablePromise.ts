/**
 * This class represents a way to cancel a promise for a specific reason provided in the constructor.
 * The promise will be rejected without throwing so anything awaiting that promise immediately continues.
 */
export class CancelToken {
  private _rejects: ((reason: unknown) => void)[] = [];
  private _isCancelled = false;

  constructor(public Reason: unknown) {}

  /**
   * Register a reject call from a Promise.
   * The reject function will be called using this CancelToken's reason when its Cancel function is called
   * @param reject
   */
  public Register(reject: (reason: unknown) => void): void {
    this._rejects.push(reject);
  }

  /**
   * Unregister a reject call from a Promise.
   * The reject function will no longer be called using this CancelToken's reason when its Cancel function is called
   * @param reject
   */
  public Unregister(reject: (reason: unknown) => void): void {
    const rejectionIndex = this._rejects.indexOf(reject);
    if (rejectionIndex >= 0) {
      this._rejects.splice(rejectionIndex, 1);
    }
  }

  public get IsCancelled(): boolean {
    return this._isCancelled;
  }

  /**
   * Cancels any relevant CancellablePromise by cleanly rejecting it
   */
  public Cancel(): void {
    if (this._isCancelled) {
      return;
    }
    for (const reject of this._rejects) {
      reject(this.Reason);
    }
    this._isCancelled = true;
  }
}

/**
 * Function to construct a Promise with a CancelToken that can be used to cancel the promise
 * @param executor Regular executor to be passed into Promise
 * @param cancelToken CancelToken used to cancel the promise
 * @returns
 */
export async function CancellablePromise<T>(
  executor: (
    resolve: (value: T | PromiseLike<T>) => void,
    reject: (reason: unknown) => void
  ) => void,
  ...cancelTokens: CancelToken[]
) {
  let cancel: (() => void) | null = null;
  try {
    return await new Promise<T>((resolve, reject) => {
      cancel = reject;
      for (const cancelToken of cancelTokens) {
        cancelToken.Register(cancel);
      }

      if (cancelTokens.some(cancelToken => cancelToken.IsCancelled)) {
        reject();
      } else {
        executor(resolve, reject);
      }
    });
  } catch (error) {
    if (!cancelTokens.some(cancelToken => error === cancelToken.Reason)) {
      throw error;
    }
  } finally {
    if (cancel) {
      for (const cancelToken of cancelTokens) {
        cancelToken.Unregister(cancel);
      }
    }
  }
  return undefined;
}

/**
 * Function to construct a Promise race with a CancelToken that can be used to cancel the outer promise
 * @param promises Promises to race
 * @param cancelToken CancelToken used to cancel the promise
 * @returns
 */
export async function CancellablePromiseRace<T>(
  promises: Promise<T>[],
  ...cancelTokens: CancelToken[]
) {
  let cancel: (() => void) | null = null;
  try {
    return await Promise.race([
      ...promises,
      new Promise<T>((_, reject) => {
        cancel = reject;
        for (const cancelToken of cancelTokens) {
          cancelToken.Register(cancel);
        }
        if (cancelTokens.some(cancelToken => cancelToken.IsCancelled)) {
          reject();
        }
      })
    ]);
  } catch (error) {
    if (!cancelTokens.some(cancelToken => error === cancelToken.Reason)) {
      throw error;
    }
  } finally {
    if (cancel) {
      for (const cancelToken of cancelTokens) {
        cancelToken.Unregister(cancel);
      }
    }
  }
  return undefined;
}
