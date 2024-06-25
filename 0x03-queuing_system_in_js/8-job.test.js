import { expect } from 'chai';
import Queue from 'kue';
import createPushNotificationsJobs from './createPushNotificationsJobs'; // Assuming it's in the same directory

// Initialize Kue queue
const queue = new Queue();

describe('createPushNotificationsJobs', () => {
  // Enter test mode without processing jobs before tests
  before(() => {
    queue.testMode.enter();
  });

  // Clear the queue and exit test mode after tests
  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
    const result = createPushNotificationsJobs(null);
    expect(result).to.equal('Jobs is not an array');
  });

  it('should create two new jobs in the queue', () => {
    const jobs = [{ phoneNumber: '1234567890', message: 'Hello' }, { phoneNumber: '9876543210', message: 'Hi' }];
    createPushNotificationsJobs(jobs);
    const jobsInQueue = queue.testMode.jobs;
    expect(jobsInQueue).to.have.lengthOf(2);
    expect(jobsInQueue[0].type).to.equal('push_notification_code_3');
    expect(jobsInQueue[1].type).to.equal('push_notification_code_3');
    // Additional assertions as needed
  });
});
